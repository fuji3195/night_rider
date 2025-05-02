// sync_reset.v
module sync_reset (
    input clk,      // system clock
    input async_n,  // 非同期Reset入力 (ボタンなど)
    output reg sync_n
);

    reg meta;   // 2段階フリップフロップで同期化

    always @(posedge clk or negedge async_n) begin
        if (!async_n) begin
            // 非同期リセット
            meta <= 1'b0;
            sync_n <= 1'b0;
        end else begin
            // 同期リセット
            meta <= 1'b1;
            sync_n <= meta;
        end
    end
endmodule

