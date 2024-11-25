
module BigCircle(output G, P, input Gi, Pi, GiPrev, PiPrev);
  wire e;
  and (e, Pi, GiPrev);
  or (G, e, Gi);
  and (P, Pi, PiPrev);
endmodule

module SmallCircle(output Ci, input Gi);
  buf (Ci, Gi);
endmodule

module Square(output G, P, input Ai, Bi);
  and (G, Ai, Bi);
  xor (P, Ai, Bi);
endmodule

module Triangle(output Si, input Pi, CiPrev);
  xor (Si, Pi, CiPrev);
endmodule


module adder_8b_5l(output [7:0] sum, output cout, input [7:0] a, b);

  wire cin = 1'b0;
  wire [7:0] c;
  wire [7:0] g, p;
  Square sq[7:0](g, p, a, b);

  wire [16:8] g2, p2;
  BigCircle bc2_8(g2[8], p2[8], g[1], p[1], g[0], p[0]);
  BigCircle bc2_10(g2[10], p2[10], g[3], p[3], g[2], p[2]);
  BigCircle bc2_13(g2[13], p2[13], g[5], p[5], g[4], p[4]);
  BigCircle bc2_16(g2[16], p2[16], g[7], p[7], g[6], p[6]);

  wire [11:9] g3, p3;
  BigCircle bc3_9(g3[9], p3[9], g[2], p[2], g2[8], p2[8]);
  BigCircle bc3_11(g3[11], p3[11], g2[10], p2[10], g2[8], p2[8]);

  wire [14:12] g4, p4;
  BigCircle bc4_12(g4[12], p4[12], g[4], p[4], g3[11], p3[11]);
  BigCircle bc4_14(g4[14], p4[14], g2[13], p2[13], g3[11], p3[11]);

  wire [17:15] g5, p5;
  BigCircle bc5_15(g5[15], p5[15], g[6], p[6], g4[14], p4[14]);
  BigCircle bc5_17(g5[17], p5[17], g2[16], p2[16], g4[14], p4[14]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[8]);
  SmallCircle sc2(c[2], g3[9]);
  SmallCircle sc3(c[3], g3[11]);
  SmallCircle sc4(c[4], g4[12]);
  SmallCircle sc5(c[5], g4[14]);
  SmallCircle sc6(c[6], g5[15]);
  SmallCircle sc7(c[7], g5[17]);
  Triangle tr0(sum[0], p[0], cin);
  Triangle tr1(sum[1], p[1], c[0]);
  Triangle tr2(sum[2], p[2], c[1]);
  Triangle tr3(sum[3], p[3], c[2]);
  Triangle tr4(sum[4], p[4], c[3]);
  Triangle tr5(sum[5], p[5], c[4]);
  Triangle tr6(sum[6], p[6], c[5]);
  Triangle tr7(sum[7], p[7], c[6]);

  buf (cout, c[7]);

endmodule