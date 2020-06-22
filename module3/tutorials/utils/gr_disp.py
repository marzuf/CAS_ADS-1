"""Utility for displaying Tensorflow graphs.
"""
import tensorflow as tf
import numpy as np
from IPython.display import display, HTML


def show(graph_def, grouping_character='_'):
    """

    :GraphDef graph_def: tensorflow graph definition
    :string grouping_character: sub-levels split character
    """
    # Helper functions for TF Graph visualization

    def _drop_long_consts(_graph_def, max_const_size=32):
        """Strip large constant values from _graph_def.
        :GraphDef _graph_def: tensorflow graph definition
        :int max_const_size: maximal constants size to keep
        :return: GraphDef
        """
        strip_def = tf.GraphDef()
        for n0 in _graph_def.node:
            n = strip_def.node.add()
            n.MergeFrom(n0)
            if n.op == 'Const':
                tensor = n.attr['value'].tensor
                size = len(tensor.tensor_content)
                if size > max_const_size:
                    tensor.tensor_content = "<tensor content size {} b>".format(size).encode()
        return strip_def

    def _rename_nodes(_graph_def, rename_func):
        """Rename nodes grouping for better appearance"""
        res_def = tf.GraphDef()
        for n0 in _graph_def.node:
            n = res_def.node.add()
            n.MergeFrom(n0)
            n.name = rename_func(n.name)
            for i, s in enumerate(n.input):
                n.input[i] = rename_func(s) if s[0] != '^' else '^' + rename_func(s[1:])
        return res_def

    def _show_graph(_graph_def, max_const_size=32):
        """Get TensorFlow GraphDef and display using TensorBoard.
        :GraphDef _graph_def: tensorflow graph definition
        :int max_const_size: maximal constants size to keep
        :return: GraphDef
        """
        if hasattr(_graph_def, 'as_graph_def'):
            _graph_def = _graph_def.as_graph_def()

        short_graph_def = _drop_long_consts(_graph_def, max_const_size=max_const_size)
        tb_display_code = """
            <script>
              function load() {{
                document.getElementById("{id}").pbtxt = {data};
              }}
            </script>
            <link rel="import" href="https://tensorboard.appspot.com/tf-graph-basic.build.html" onload=load()>
            <div style="height:600px">
              <tf-graph-basic id="{id}"></tf-graph-basic>
            </div>
        """.format(data=repr(str(short_graph_def)), id='graph' + str(np.random.rand()))

        iframe = """
            <iframe seamless style="width:800px;height:620px;border:0" srcdoc="{}"></iframe>
        """.format(tb_display_code.replace('"', '&quot;'))
        display(HTML(iframe))

    tmp_def = _rename_nodes(graph_def, lambda s: "/".join(s.split(grouping_character, 1)))
    _show_graph(tmp_def)
