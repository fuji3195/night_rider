// top module
module night_rider_fsm 
    # (parameter N = 8)
(
    input clk,
    input rst_n,
    output [N-1:0] led_out 
);

    localparam add_N = $clog2(N);
    localparam [add_N-1:0] N_MINUS_2 = (N - 2)[add_N-1:0];
    localparam [1:0] LIGHT_FIRST = 2'b01,
                    LIGHT_MID = 2'b10,
                    LIGHT_LAST = 2'b11;
    
    reg [add_N-1:0] n;
    reg dir;
    reg [1:0] state;

    assign led_out = 1'b1<<n; 

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= LIGHT_FIRST;
            n <= 0;
            dir <= 1;
        end
        else  begin
            case (state)
                LIGHT_FIRST: begin n <= n + 1; state <= LIGHT_MID; end
                LIGHT_LAST : begin n <= n - 1; state <= LIGHT_MID; end
                LIGHT_MID  : begin
                        if (dir == 1'b1) begin
                            n <= n + 1;
                            if (n == N_MINUS_2) begin dir <= 0; state <= LIGHT_LAST; end
                        end
                        else begin
                            n <= n - 1;
                            if (n == 1) begin dir <= 1; state <= LIGHT_FIRST; end
                        end
                    end
                default: begin state <= LIGHT_FIRST; n <= 0; dir <= 1; end
            endcase
        end
    end
endmodule


