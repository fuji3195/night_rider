// countup module
`timescale 10ns/10ps
module test (
    input wire clk,
    input wire rst_n,
    output reg [7:0] count
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) count <= 0;
        else count <= count + 1;
    end
endmodule