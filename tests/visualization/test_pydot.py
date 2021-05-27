# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import tempfile
import unittest

import retworkx
from retworkx.visualization import pydot_draw

try:
    import pydot
    import PIL

    pydot.call_graphviz("dot", ["--version"], tempfile.gettempdir())
    HAS_PYDOT = True
except Exception:
    HAS_PYDOT = False

SAVE_IMAGES = os.getenv("RETWORKX_TEST_PRESERVE_IMAGES", None)


def _save_image(image, path):
    if SAVE_IMAGES:
        image.save(path)


@unittest.skipUnless(
    HAS_PYDOT, "pydot and graphviz are required for running these tests"
)
class TestPyDotDraw(unittest.TestCase):
    def test_draw_no_args(self):
        graph = retworkx.generators.star_graph(24)
        image = pydot_draw(graph)
        self.assertIsInstance(image, PIL.Image.Image)
        _save_image(image, "test_pydot_draw.png")

    def test_draw_node_attr_fn(self):
        graph = retworkx.PyGraph()
        graph.add_node(
            {
                "color": "black",
                "fillcolor": "green",
                "label": "a",
                "style": "filled",
            }
        )
        graph.add_node(
            {
                "color": "black",
                "fillcolor": "red",
                "label": "a",
                "style": "filled",
            }
        )
        graph.add_edge(0, 1, dict(label="1", name="1"))
        image = pydot_draw(graph, lambda node: node)
        self.assertIsInstance(image, PIL.Image.Image)
        _save_image(image, "test_pydot_draw_node_attr.png")

    def test_draw_edge_attr_fn(self):
        graph = retworkx.PyGraph()
        graph.add_node(
            {
                "color": "black",
                "fillcolor": "green",
                "label": "a",
                "style": "filled",
            }
        )
        graph.add_node(
            {
                "color": "black",
                "fillcolor": "red",
                "label": "a",
                "style": "filled",
            }
        )
        graph.add_edge(0, 1, dict(label="1", name="1"))
        image = pydot_draw(graph, lambda node: node, lambda edge: edge)
        self.assertIsInstance(image, PIL.Image.Image)
        _save_image(image, "test_pydot_draw_edge_attr.png")

    def test_draw_graph_attr(self):
        graph = retworkx.PyGraph()
        graph.add_node(
            {
                "color": "black",
                "fillcolor": "green",
                "label": "a",
                "style": "filled",
            }
        )
        graph.add_node(
            {
                "color": "black",
                "fillcolor": "red",
                "label": "a",
                "style": "filled",
            }
        )
        graph.add_edge(0, 1, dict(label="1", name="1"))
        graph_attr = {"bgcolor": "red"}
        image = pydot_draw(
            graph, lambda node: node, lambda edge: edge, graph_attr
        )
        self.assertIsInstance(image, PIL.Image.Image)
        _save_image(image, "test_pydot_draw_graph_attr.png")

    def test_image_type(self):
        graph = retworkx.directed_gnp_random_graph(50, 0.8)
        image = pydot_draw(graph, image_type="jpg")
        self.assertIsInstance(image, PIL.Image.Image)
        _save_image(image, "test_pydot_draw_image_type.jpg")

    def test_method(self):
        graph = retworkx.directed_gnp_random_graph(50, 0.8)
        image = pydot_draw(graph, method="sfdp")
        self.assertIsInstance(image, PIL.Image.Image)
        _save_image(image, "test_pydot_method.png")

    def test_filename(self):
        graph = retworkx.generators.grid_graph(20, 20)
        pydot_draw(
            graph,
            filename="test_pydot_filename.svg",
            image_type="svg",
            method="neato",
        )
        self.assertTrue(os.path.isfile("test_pydot_filename.svg"))
        if not SAVE_IMAGES:
            self.addCleanup(os.remove, "test_pydot_filename.svg")