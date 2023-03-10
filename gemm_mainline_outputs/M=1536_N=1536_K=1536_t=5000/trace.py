from tvm import tir
from tvm.tir import floordiv, floormod
# from tvm import tir
def apply_trace(sch: tir.Schedule) -> None:
  b0 = sch.get_block(name="Y", func_name="main")
  b1 = sch.get_block(name="root", func_name="main")
  sch.annotate(block_or_loop=b0, ann_key="meta_schedule.tiling_structure", ann_val="SSSRRSRS")
  l2, l3, l4 = sch.get_loops(block=b0)
  v5, v6, v7, v8, v9 = sch.sample_perfect_tile(loop=l2, n=5, max_innermost_factor=64, decision=[32, 1, 2, 8, 3])
  l10, l11, l12, l13, l14 = sch.split(loop=l2, factors=[v5, v6, v7, v8, v9], preserve_unit_iters=True)
  v15, v16, v17, v18, v19 = sch.sample_perfect_tile(loop=l3, n=5, max_innermost_factor=64, decision=[12, 1, 32, 1, 4])
  l20, l21, l22, l23, l24 = sch.split(loop=l3, factors=[v15, v16, v17, v18, v19], preserve_unit_iters=True)
  v25, v26, v27 = sch.sample_perfect_tile(loop=l4, n=3, max_innermost_factor=64, decision=[192, 1, 8])
  l28, l29, l30 = sch.split(loop=l4, factors=[v25, v26, v27], preserve_unit_iters=True)
  sch.reorder(l10, l20, l11, l21, l12, l22, l28, l29, l13, l23, l30, l14, l24)
  l31 = sch.fuse(l10, l20, preserve_unit_iters=True)
  sch.bind(loop=l31, thread_axis="blockIdx.x")
  l32 = sch.fuse(l11, l21, preserve_unit_iters=True)
  sch.bind(loop=l32, thread_axis="vthread.x")
  l33 = sch.fuse(l12, l22, preserve_unit_iters=True)
  sch.bind(loop=l33, thread_axis="threadIdx.x")
  sch.annotate(block_or_loop=b0, ann_key="meta_schedule.thread_extent_low_inclusive", ann_val=32)
  sch.annotate(block_or_loop=b0, ann_key="meta_schedule.thread_extent_high_inclusive", ann_val=1024)
  b34 = sch.cache_write(block=b0, write_buffer_index=0, storage_scope="local")
  sch.reverse_compute_at(block=b34, loop=l33, preserve_unit_loops=True, index=-1)
  b35 = sch.cache_read(block=b0, read_buffer_index=0, storage_scope="shared", consumer_blocks=[b0])
  sch.compute_at(block=b35, loop=l28, preserve_unit_loops=True, index=-1)
  l36, l37, l38, l39, l40, l41 = sch.get_loops(block=b35)
  l42 = sch.fuse(l40, l41, preserve_unit_iters=True)
  v43 = sch.sample_categorical(candidates=[1, 2, 3, 4], probs=[0.25, 0.25, 0.25, 0.25], decision=1)
  sch.annotate(block_or_loop=b35, ann_key="meta_schedule.cooperative_fetch", ann_val=v43)
  b44 = sch.cache_read(block=b0, read_buffer_index=1, storage_scope="shared", consumer_blocks=[b0])
  sch.compute_at(block=b44, loop=l28, preserve_unit_loops=True, index=-1)
  l45, l46, l47, l48, l49, l50 = sch.get_loops(block=b44)
  l51 = sch.fuse(l49, l50, preserve_unit_iters=True)
  v52 = sch.sample_categorical(candidates=[1, 2, 3, 4], probs=[0.25, 0.25, 0.25, 0.25], decision=3)
  sch.annotate(block_or_loop=b44, ann_key="meta_schedule.cooperative_fetch", ann_val=v52)
  v53 = sch.sample_categorical(candidates=[0, 16, 64, 512, 1024], probs=[0.20000000000000001, 0.20000000000000001, 0.20000000000000001, 0.20000000000000001, 0.20000000000000001], decision=4)
  sch.annotate(block_or_loop=b1, ann_key="meta_schedule.unroll_explicit", ann_val=v53)
  sch.enter_postproc()
  sch.unannotate(block_or_loop=b35, ann_key="meta_schedule.cooperative_fetch")
  l54, l55, l56, l57, l58 = sch.get_loops(block=b35)
  l59, l60, l61 = sch.split(loop=l58, factors=[None, 64, 2], preserve_unit_iters=True)
  sch.vectorize(loop=l61)
  sch.bind(loop=l60, thread_axis="threadIdx.x")
  sch.unannotate(block_or_loop=b44, ann_key="meta_schedule.cooperative_fetch")
  l62, l63, l64, l65, l66 = sch.get_loops(block=b44)
  l67, l68, l69 = sch.split(loop=l66, factors=[None, 64, 4], preserve_unit_iters=True)
  sch.vectorize(loop=l69)
  sch.bind(loop=l68, thread_axis="threadIdx.x")
  b70 = sch.get_block(name="root", func_name="main")
  sch.unannotate(block_or_loop=b70, ann_key="meta_schedule.unroll_explicit")
  b71, b72, b73, b74 = sch.get_child_blocks(b70)
  l75, l76, l77, l78, l79, l80, l81 = sch.get_loops(block=b71)
  sch.annotate(block_or_loop=l75, ann_key="pragma_auto_unroll_max_step", ann_val=1024)
  sch.annotate(block_or_loop=l75, ann_key="pragma_unroll_explicit", ann_val=1)
  l82, l83, l84, l85, l86, l87, l88 = sch.get_loops(block=b72)
  sch.annotate(block_or_loop=l82, ann_key="pragma_auto_unroll_max_step", ann_val=1024)
  sch.annotate(block_or_loop=l82, ann_key="pragma_unroll_explicit", ann_val=1)
  l89, l90, l91, l92, l93, l94, l95, l96, l97, l98 = sch.get_loops(block=b73)
  sch.annotate(block_or_loop=l89, ann_key="pragma_auto_unroll_max_step", ann_val=1024)
  sch.annotate(block_or_loop=l89, ann_key="pragma_unroll_explicit", ann_val=1)
  l99, l100, l101, l102, l103 = sch.get_loops(block=b74)
  sch.annotate(block_or_loop=l99, ann_key="pragma_auto_unroll_max_step", ann_val=1024)
  sch.annotate(block_or_loop=l99, ann_key="pragma_unroll_explicit", ann_val=1)
  b104 = sch.get_block(name="Y", func_name="main")
  l105, l106, l107, l108, l109, l110, l111, l112, l113, l114 = sch.get_loops(block=b104)
  b115 = sch.decompose_reduction(block=b104, loop=l108)
