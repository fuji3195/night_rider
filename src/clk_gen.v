module clk_divideby_27 #(parameter DIV = 27) (
    input clk_in,
    input rst_n,
    output reg clk_out = 0
);

    integer cnt = 0;
    always @(posedge clk_in or negedge rst_n) begin
        if (!rst_n) begin
            cnt <= 0;
            clk_out <= 0;
        end else if (cnt == DIV/2-1) begin
            cnt <= 0;
            clk_out <= ~clk_out;
        end else begin
            cnt <= cnt + 1;
        end
    end
endmodule

module clk_divideby_100K (
    input clk_in,
    input rst_n,
    output reg clk_out = 0
);
`ifdef SIM
    localparam integer div = 10;    // 100KHz
`else
    localparam integer div = 100000;    // 10 Hz
`endif
    integer cnt = 0;
    always @(posedge clk_in or negedge rst_n) begin
        if (!rst_n) begin
            cnt <= 0;
            clk_out <= 0;
        end else if (cnt ==div/2-1) begin
            cnt <= 0;
            clk_out <= ~clk_out;
        end else begin
            cnt <= cnt + 1;
        end
    end
endmodule