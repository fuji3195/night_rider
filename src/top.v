module top 
    # (parameter N = 8)
(
    input board_clk,
    input rst_n_btn,
    output [N-1:0] led
);

    wire sys_clk;
    wire clk_10hz;
    wire rst_sync;

    // 27M --> 1M
    clk_divideby_27 divide_to_1MHz (
        .clk_in(board_clk),
        .rst_n(rst_n_btn),
        .clk_out(sys_clk)
    );

    clk_divideby_100K divide_to_10Hz (
        .clk_in(sys_clk),
        .rst_n(rst_n_btn),
        .clk_out(clk_10hz)
    );

    sync_reset u_sync_reset (
        .clk(clk_10hz),
        .async_n(rst_n_btn),
        .sync_n(rst_sync)
    );

    night_rider_fsm #(.N(N)) u_night (
        .clk (clk_10hz),
        .rst_n(rst_sync),
        .led_out(led)
    );

endmodule