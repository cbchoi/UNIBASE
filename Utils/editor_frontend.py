# pip install dearpygui
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
import uuid
import json
import dearpygui.dearpygui as dpg

# ---------- Model ----------
@dataclass
class PortSpec:
    name: str
    direction: str  # "in" | "out"
    dtype: str      # 예: "float", "image", "event"
    tag: Optional[str] = None

@dataclass
class NodeModel:
    node_type: str
    title: str
    pos: Tuple[int, int] = (100, 100)
    inner_size: Tuple[int, int] = (280, 160)  # child_window 크기(커스텀 리사이즈 대상)
    attrs: Dict[str, str] = field(default_factory=dict)  # 유저 파라미터
    inputs: List[PortSpec] = field(default_factory=list)
    outputs: List[PortSpec] = field(default_factory=list)
    tag: str = field(default_factory=lambda: f"node:{uuid.uuid4()}")
    # 런타임용(뷰 바인딩 후 결정)
    editor_tag: Optional[str] = None
    child_tag: Optional[str] = None

    def to_json(self) -> str:
        # tag 등 런타임 태그도 저장할 수 있으나, 재생성 시 새로 배정 권장
        serializable = asdict(self)
        return json.dumps(serializable)

    @staticmethod
    def from_json(s: str) -> "NodeModel":
        data = json.loads(s)
        return NodeModel(**data)

# ---------- Controller + View ----------
class NodeView:
    def __init__(self, model: NodeModel):
        self.m = model
        self._resizing = False
        self._start_mouse = (0, 0)
        self._start_size = self.m.inner_size

    # --- 내부 유틸 ---
    @staticmethod
    def _mk_port_tag() -> str:
        return f"port:{uuid.uuid4()}"

    def _on_grip_pressed(self, sender, app_data, user_data):
        self._resizing = True
        self._start_mouse = dpg.get_mouse_pos()
        self._start_size = (dpg.get_item_width(self.m.child_tag),
                            dpg.get_item_height(self.m.child_tag))

        print("###+")

    def on_mouse_move(self):
        if not self._resizing or not dpg.does_item_exist(self.m.child_tag):
            return
        mx, my = dpg.get_mouse_pos()
        sx, sy = self._start_mouse
        w0, h0 = self._start_size
        new_w = max(140, int(w0 + (mx - sx)))
        new_h = max(100, int(h0 + (my - sy)))
        dpg.set_item_width(self.m.child_tag, new_w)
        dpg.set_item_height(self.m.child_tag, new_h)
        self.m.inner_size = (new_w, new_h)

    def on_mouse_release(self):
        self._resizing = False
        print("###+11")

    # --- 포트 생성 ---
    def _build_ports(self):
        # 출력 포트
        for p in self.m.outputs:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, parent=self.m.tag) as attr:
                p.tag = p.tag or self._mk_port_tag()
                dpg.add_text(p.name)
                dpg.add_spacer(height=2)
                dpg.add_text(f"({p.dtype})", bullet=True)
                dpg.bind_item_theme(attr, "port_out_theme") if dpg.does_item_exist("port_out_theme") else None

        # 입력 포트
        for p in self.m.inputs:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, parent=self.m.tag) as attr:
                p.tag = p.tag or self._mk_port_tag()
                dpg.add_text(p.name)
                dpg.add_spacer(height=2)
                dpg.add_text(f"({p.dtype})", bullet=True)
                dpg.bind_item_theme(attr, "port_in_theme") if dpg.does_item_exist("port_in_theme") else None

    # --- 뷰 생성/파괴 ---
    def create(self, editor_tag: str):
        self.m.editor_tag = editor_tag
        with dpg.node(label=self.m.title, parent=editor_tag, pos=self.m.pos, tag=self.m.tag):
            # Static area: 리사이즈 가능한 콘텐츠 영역 + 그립
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                self.m.child_tag = f"child:{uuid.uuid4()}"
                dpg.add_child_window(tag=self.m.child_tag, width=self.m.inner_size[0],
                                     height=self.m.inner_size[1], border=True)
                # 그립(우하단)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=max(0, self.m.inner_size[0]-40))
                    dpg.add_button(label="◢", width=28, height=24,
                                   callback=self._on_grip_pressed)
                    print("@@@")

            # 사용자 속성(예: 파라미터) 영역
            #with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            #    for k, v in self.m.attrs.items():
            #        dpg.add_input_text(label=k, default_value=str(v),
            #                           callback=lambda s,a,u,k=k: self._on_attr_changed(k, a))

            self._build_ports()

    def destroy(self):
        if dpg.does_item_exist(self.m.tag):
            dpg.delete_item(self.m.tag)

    def _on_attr_changed(self, key: str, app_data):
        self.m.attrs[key] = app_data

    # 선택/위치 동기화
    def sync_position_from_ui(self):
        if dpg.does_item_exist(self.m.tag):
            self.m.pos = tuple(dpg.get_node_pos(self.m.tag))

# ---------- Registry & Link Rules ----------
class GraphController:
    """노드·링크 수명주기와 타입 검증, 직렬화 담당"""
    def __init__(self, editor_tag: str):
        self.editor_tag = editor_tag
        self.nodes: Dict[str, NodeView] = {}   # key=node_tag
        self.links: Dict[str, Tuple[str, str]] = {}  # link_tag -> (src_port, dst_port)

    def add_node(self, model: NodeModel) -> NodeView:
        v = NodeView(model)
        v.create(self.editor_tag)
        self.nodes[model.tag] = v
        return v

    def delete_selected(self):
        for node_tag in dpg.get_selected_nodes(self.editor_tag):
            if node_tag in self.nodes:
                self.nodes[node_tag].destroy()
                self.nodes.pop(node_tag, None)

    def link_callback(self, sender, app_data, user_data):
        src_attr, dst_attr = app_data  # attr tags
        if not self._link_allowed(src_attr, dst_attr):
            return  # 규칙 불일치 시 링크 생성 안 함
        link_tag = f"link:{uuid.uuid4()}"
        dpg.add_node_link(src_attr, dst_attr, parent=self.editor_tag, tag=link_tag)
        self.links[link_tag] = (src_attr, dst_attr)

    def delink_callback(self, sender, app_data, user_data):
        # app_data == link_tag
        self.links.pop(app_data, None)
        dpg.delete_item(app_data)

    # 포트 타입 검증(예시)
    def _link_allowed(self, src_attr: str, dst_attr: str) -> bool:
        # 실제로는 port-tag -> PortSpec 매핑 테이블을 유지하고 dtype/방향 검증
        # 여기서는 간단히: out->in 만 허용
        try:
            st = dpg.get_item_type(src_attr)
            dt = dpg.get_item_type(dst_attr)
        except Exception:
            return False
        # NodeAttribute는 방향 정보를 직접 주지 않으므로, 생성 시 PortSpec 테이블로 검증하는 것이 정석.
        return True

    # 직렬화
    def dump_json(self) -> str:
        for v in self.nodes.values():
            v.sync_position_from_ui()
        payload = {
            "nodes": [json.loads(v.m.to_json()) for v in self.nodes.values()],
            "links": [{"tag": k, "endpoints": v} for k, v in self.links.items()]
        }
        return json.dumps(payload, indent=2)

    def load_json(self, s: str):
        data = json.loads(s)
        # 기존 정리
        for k in list(self.nodes.keys()):
            self.nodes[k].destroy()
            self.nodes.pop(k)
        for ltag in list(self.links.keys()):
            dpg.delete_item(ltag)
            self.links.pop(ltag)

        # 노드 재생성
        for nd in data.get("nodes", []):
            m = NodeModel(**nd)
            self.add_node(m)

        # 링크 재생성 (주의: 포트 tag가 재사용되도록 설계해야 함)
        for l in data.get("links", []):
            src, dst = l["endpoints"]
            if dpg.does_item_exist(src) and dpg.does_item_exist(dst):
                dpg.add_node_link(src, dst, parent=self.editor_tag, tag=l["tag"])
                self.links[l["tag"]] = (src, dst)

# ---------- Bootstrap ----------
def build_demo():
    dpg.create_context()

    with dpg.handler_registry():
        # 런타임 핸들러는 각 NodeView 인스턴스에 연결할 수도 있으나,
        # 간단하게 전체 그래프에 대해 브로드캐스트
        dpg.add_mouse_move_handler(callback=lambda: [
            v.on_mouse_move() for v in GC.nodes.values()
        ])
        dpg.add_mouse_release_handler(callback=lambda: [
            v.on_mouse_release() for v in GC.nodes.values()
        ])

    with dpg.window(label="Node Editor", width=1000, height=700):
        editor = dpg.add_node_editor(callback=lambda s,a,u: GC.link_callback(s,a,u),
                                     delink_callback=lambda s,a,u: GC.delink_callback(s,a,u))
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="Add Source", callback=lambda: GC.add_node(
                NodeModel(
                    node_type="Source",
                    title="Source",
                    outputs=[PortSpec("out", "out", "float")],
                    attrs={"rate":"10Hz"}
                )
            ))
            dpg.add_button(label="Add Sink", callback=lambda: GC.add_node(
                NodeModel(
                    node_type="Sink",
                    title="Sink",
                    inputs=[PortSpec("in", "in", "float")],
                    attrs={"buffer":"16"}
                )
            ))
            dpg.add_button(label="Delete Selected", callback=lambda: GC.delete_selected())
            dpg.add_button(label="Save JSON", callback=lambda: print(GC.dump_json()))

    # 테마(선택)
    with dpg.theme(tag="port_in_theme"):
        with dpg.theme_component(dpg.mvNode_Attr_Input):
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (40, 60, 80), category=dpg.mvThemeCat_Nodes)
    with dpg.theme(tag="port_out_theme"):
        with dpg.theme_component(dpg.mvNode_Attr_Output):
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (80, 60, 40), category=dpg.mvThemeCat_Nodes)

    global GC
    GC = GraphController(editor)

    dpg.create_viewport(title="Node Class Demo", width=1100, height=760)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

build_demo()
