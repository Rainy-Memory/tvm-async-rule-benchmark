# from tvm.script import tir as T
@tvm.script.ir_module
class Module:
    @T.prim_func
    def main(A: T.Buffer[(512, 256), "float32"], B: T.Buffer[(256, 384), "float32"], Y: T.Buffer[(512, 384), "float32"]):
        # function attr dict
        T.func_attr({"global_symbol": "main", "tir.noalias": True})
        # body
        # with T.block("root")
        Y_local = T.alloc_buffer([512, 384], dtype="float32", scope="local")
        A_shared = T.alloc_buffer([512, 256], dtype="float32", scope="shared")
        B_shared = T.alloc_buffer([256, 384], dtype="float32", scope="shared")
        for i_0_j_0_fused in T.thread_binding(64, thread="blockIdx.x", annotations={"pragma_auto_unroll_max_step":1024, "pragma_unroll_explicit":1}):
            for i_1_j_1_fused in T.thread_binding(3, thread="vthread.x"):
                for i_2_j_2_fused in T.thread_binding(128, thread="threadIdx.x"):
                    for i_3_init, j_3_init, i_4_init, j_4_init in T.grid(1, 1, 8, 1):
                        with T.block("Y_init"):
                            v_i = T.axis.spatial(512, i_0_j_0_fused // 8 * 64 + i_2_j_2_fused // 16 * 8 + i_3_init * 8 + i_4_init)
                            v_j = T.axis.spatial(384, i_0_j_0_fused % 8 * 48 + i_1_j_1_fused * 16 + i_2_j_2_fused % 16 + j_3_init + j_4_init)
                            T.reads()
                            T.writes(Y_local[v_i, v_j])
                            T.block_attr({"meta_schedule.thread_extent_high_inclusive":1024, "meta_schedule.thread_extent_low_inclusive":32, "meta_schedule.tiling_structure":"SSSRRSRS"})
                            Y_local[v_i, v_j] = T.float32(0)
                    for k_0_fused in T.serial(8, annotations={"software_pipeline_async_stages":[0], "software_pipeline_order":[0, 1, 2], "software_pipeline_stage":[0, 0, 2]}):
                        for ax0_ax1_fused_0 in T.serial(4):
                            for ax0_ax1_fused_1 in T.thread_binding(128, thread="threadIdx.x"):
                                for ax0_ax1_fused_2 in T.vectorized(4):
                                    with T.block("A_shared"):
                                        v0 = T.axis.spatial(512, i_0_j_0_fused // 8 * 64 + (ax0_ax1_fused_0 * 512 + ax0_ax1_fused_1 * 4 + ax0_ax1_fused_2) // 32)
                                        v1 = T.axis.spatial(256, k_0_fused * 32 + (ax0_ax1_fused_0 * 512 + ax0_ax1_fused_1 * 4 + ax0_ax1_fused_2) % 32)
                                        T.reads(A[v0, v1])
                                        T.writes(A_shared[v0, v1])
                                        A_shared[v0, v1] = A[v0, v1]
                        for ax0_ax1_fused_0 in T.serial(3):
                            for ax0_ax1_fused_1 in T.thread_binding(128, thread="threadIdx.x"):
                                for ax0_ax1_fused_2 in T.vectorized(4):
                                    with T.block("B_shared"):
                                        v0 = T.axis.spatial(256, k_0_fused * 32 + (ax0_ax1_fused_0 * 512 + ax0_ax1_fused_1 * 4 + ax0_ax1_fused_2) // 48)
                                        v1 = T.axis.spatial(384, i_0_j_0_fused % 8 * 48 + (ax0_ax1_fused_0 * 512 + ax0_ax1_fused_1 * 4 + ax0_ax1_fused_2) % 48)
                                        T.reads(B[v0, v1])
                                        T.writes(B_shared[v0, v1])
                                        B_shared[v0, v1] = B[v0, v1]
                        for k_1, i_3, j_3, k_2, i_4, j_4 in T.grid(4, 1, 1, 8, 8, 1):
                            with T.block("Y_update"):
                                v_i = T.axis.spatial(512, i_0_j_0_fused // 8 * 64 + i_2_j_2_fused // 16 * 8 + i_3 * 8 + i_4)
                                v_j = T.axis.spatial(384, i_0_j_0_fused % 8 * 48 + i_1_j_1_fused * 16 + i_2_j_2_fused % 16 + j_3 + j_4)
                                v_k = T.axis.reduce(256, k_0_fused * 32 + k_1 * 8 + k_2)
                                T.reads(Y_local[v_i, v_j], A_shared[v_i, v_k], B_shared[v_k, v_j])
                                T.writes(Y_local[v_i, v_j])
                                T.block_attr({"meta_schedule.thread_extent_high_inclusive":1024, "meta_schedule.thread_extent_low_inclusive":32, "meta_schedule.tiling_structure":"SSSRRSRS"})
                                Y_local[v_i, v_j] = Y_local[v_i, v_j] + A_shared[v_i, v_k] * B_shared[v_k, v_j]
                    for ax0, ax1 in T.grid(8, 1):
                        with T.block("Y_local"):
                            v0 = T.axis.spatial(512, i_0_j_0_fused // 8 * 64 + i_2_j_2_fused // 16 * 8 + ax0)
                            v1 = T.axis.spatial(384, i_0_j_0_fused % 8 * 48 + i_1_j_1_fused * 16 + i_2_j_2_fused % 16 + ax1)
                            T.reads(Y_local[v0, v1])
                            T.writes(Y[v0, v1])
                            Y[v0, v1] = Y_local[v0, v1]
    

