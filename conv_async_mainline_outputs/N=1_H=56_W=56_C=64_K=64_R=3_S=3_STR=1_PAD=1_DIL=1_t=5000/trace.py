# from tvm import tir
def apply_trace(sch: tir.Schedule) -> None:
  b0 = sch.get_block(name="PadInput", func_name="main")
  b1 = sch.get_block(name="conv2d_nhwc", func_name="main")
  b2 = sch.get_block(name="root", func_name="main")
  sch.annotate(block_or_loop=b1, ann_key="meta_schedule.tiling_structure", ann_val="SSSRRSRS")
  l3, l4, l5, l6, l7, l8, l9 = sch.get_loops(block=b1)
  v10, v11, v12, v13, v14 = sch.sample_perfect_tile(loop=l3, n=5, max_innermost_factor=64, decision=[1, 1, 1, 1, 1])
  l15, l16, l17, l18, l19 = sch.split(loop=l3, factors=[v10, v11, v12, v13, v14], preserve_unit_iters=True)
  v20, v21, v22, v23, v24 = sch.sample_perfect_tile(loop=l4, n=5, max_innermost_factor=64, decision=[4, 1, 2, 7, 1])
  l25, l26, l27, l28, l29 = sch.split(loop=l4, factors=[v20, v21, v22, v23, v24], preserve_unit_iters=True)
  v30, v31, v32, v33, v34 = sch.sample_perfect_tile(loop=l5, n=5, max_innermost_factor=64, decision=[14, 1, 2, 2, 1])
  l35, l36, l37, l38, l39 = sch.split(loop=l5, factors=[v30, v31, v32, v33, v34], preserve_unit_iters=True)
  v40, v41, v42, v43, v44 = sch.sample_perfect_tile(loop=l6, n=5, max_innermost_factor=64, decision=[1, 1, 32, 1, 2])
  l45, l46, l47, l48, l49 = sch.split(loop=l6, factors=[v40, v41, v42, v43, v44], preserve_unit_iters=True)
  v50, v51, v52 = sch.sample_perfect_tile(loop=l7, n=3, max_innermost_factor=64, decision=[1, 1, 3])
  l53, l54, l55 = sch.split(loop=l7, factors=[v50, v51, v52], preserve_unit_iters=True)
  v56, v57, v58 = sch.sample_perfect_tile(loop=l8, n=3, max_innermost_factor=64, decision=[1, 1, 3])
  l59, l60, l61 = sch.split(loop=l8, factors=[v56, v57, v58], preserve_unit_iters=True)
  v62, v63, v64 = sch.sample_perfect_tile(loop=l9, n=3, max_innermost_factor=64, decision=[16, 2, 2])
  l65, l66, l67 = sch.split(loop=l9, factors=[v62, v63, v64], preserve_unit_iters=True)
  sch.reorder(l15, l25, l35, l45, l16, l26, l36, l46, l17, l27, l37, l47, l53, l59, l65, l54, l60, l66, l18, l28, l38, l48, l55, l61, l67, l19, l29, l39, l49)
  l68 = sch.fuse(l15, l25, l35, l45, preserve_unit_iters=True)
  sch.bind(loop=l68, thread_axis="blockIdx.x")
  l69 = sch.fuse(l16, l26, l36, l46, preserve_unit_iters=True)
  sch.bind(loop=l69, thread_axis="vthread.x")
  l70 = sch.fuse(l17, l27, l37, l47, preserve_unit_iters=True)
  sch.bind(loop=l70, thread_axis="threadIdx.x")
  sch.annotate(block_or_loop=b1, ann_key="meta_schedule.thread_extent_low_inclusive", ann_val=32)
  sch.annotate(block_or_loop=b1, ann_key="meta_schedule.thread_extent_high_inclusive", ann_val=1024)
  b71 = sch.cache_write(block=b1, write_buffer_index=0, storage_scope="local")
  sch.reverse_compute_at(block=b71, loop=l70, preserve_unit_loops=True, index=-1)
  b72 = sch.cache_read(block=b1, read_buffer_index=0, storage_scope="shared", consumer_blocks=[b1])
  sch.compute_at(block=b72, loop=l65, preserve_unit_loops=True, index=-1)
  l73, l74, l75, l76, l77, l78, l79, l80, l81, l82 = sch.get_loops(block=b72)
  l83 = sch.fuse(l79, l80, l81, l82, preserve_unit_iters=True)
  v84 = sch.sample_categorical(candidates=[1, 2, 3, 4], probs=[0.25, 0.25, 0.25, 0.25], decision=0)
  sch.annotate(block_or_loop=b72, ann_key="meta_schedule.cooperative_fetch", ann_val=v84)
  b85 = sch.cache_read(block=b1, read_buffer_index=1, storage_scope="shared", consumer_blocks=[b1])
  sch.compute_at(block=b85, loop=l65, preserve_unit_loops=True, index=-1)
  l86, l87, l88, l89, l90, l91, l92, l93, l94, l95 = sch.get_loops(block=b85)
  l96 = sch.fuse(l92, l93, l94, l95, preserve_unit_iters=True)
  v97 = sch.sample_categorical(candidates=[1, 2, 3, 4], probs=[0.25, 0.25, 0.25, 0.25], decision=1)
  sch.annotate(block_or_loop=b85, ann_key="meta_schedule.cooperative_fetch", ann_val=v97)
  l98 = sch.fuse(l53, l59, l65, preserve_unit_iters=True)
  sch.annotate(block_or_loop=l98, ann_key="software_pipeline_stage", ann_val=[0, 0, 2])
  sch.annotate(block_or_loop=l98, ann_key="software_pipeline_order", ann_val=[0, 1, 2])
  sch.annotate(block_or_loop=l98, ann_key="software_pipeline_async_stages", ann_val=[0])
  sch.compute_inline(block=b0)
  v99 = sch.sample_categorical(candidates=[0, 16, 64, 512, 1024], probs=[0.20000000000000001, 0.20000000000000001, 0.20000000000000001, 0.20000000000000001, 0.20000000000000001], decision=4)
  sch.annotate(block_or_loop=b2, ann_key="meta_schedule.unroll_explicit", ann_val=v99)
  sch.enter_postproc()
  sch.unannotate(block_or_loop=b72, ann_key="meta_schedule.cooperative_fetch")
  l100, l101, l102, l103, l104 = sch.get_loops(block=b72)
  l105, l106 = sch.split(loop=l104, factors=[None, 128], preserve_unit_iters=True)
  sch.bind(loop=l106, thread_axis="threadIdx.x")
  sch.unannotate(block_or_loop=b85, ann_key="meta_schedule.cooperative_fetch")
  l107, l108, l109, l110, l111 = sch.get_loops(block=b85)
  l112, l113, l114 = sch.split(loop=l111, factors=[None, 128, 2], preserve_unit_iters=True)
  sch.vectorize(loop=l114)
  sch.bind(loop=l113, thread_axis="threadIdx.x")
  b115 = sch.get_block(name="root", func_name="main")
  sch.unannotate(block_or_loop=b115, ann_key="meta_schedule.unroll_explicit")
  b116, b117, b118, b119 = sch.get_child_blocks(b115)
  l120, l121, l122, l123, l124, l125 = sch.get_loops(block=b116)
  sch.annotate(block_or_loop=l120, ann_key="pragma_auto_unroll_max_step", ann_val=1024)
  sch.annotate(block_or_loop=l120, ann_key="pragma_unroll_explicit", ann_val=1)
  l126, l127, l128, l129, l130, l131, l132 = sch.get_loops(block=b117)
  sch.annotate(block_or_loop=l126, ann_key="pragma_auto_unroll_max_step", ann_val=1024)
  sch.annotate(block_or_loop=l126, ann_key="pragma_unroll_explicit", ann_val=1)
  l133, l134, l135, l136, l137, l138, l139, l140, l141, l142, l143, l144, l145, l146, l147, l148, l149, l150 = sch.get_loops(block=b118)
  sch.annotate(block_or_loop=l133, ann_key="pragma_auto_unroll_max_step", ann_val=1024)
  sch.annotate(block_or_loop=l133, ann_key="pragma_unroll_explicit", ann_val=1)
  l151, l152, l153, l154, l155, l156, l157 = sch.get_loops(block=b119)
  sch.annotate(block_or_loop=l151, ann_key="pragma_auto_unroll_max_step", ann_val=1024)
  sch.annotate(block_or_loop=l151, ann_key="pragma_unroll_explicit", ann_val=1)
  b158 = sch.get_block(name="conv2d_nhwc", func_name="main")
  l159, l160, l161, l162, l163, l164, l165, l166, l167, l168, l169, l170, l171, l172, l173, l174, l175, l176 = sch.get_loops(block=b158)
  b177 = sch.decompose_reduction(block=b158, loop=l162)
