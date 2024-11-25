
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


module adder_16b_7l(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [35:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_18(g2[18], p2[18], g[3], p[3], g[2], p[2]);
  BigCircle bc2_21(g2[21], p2[21], g[5], p[5], g[4], p[4]);
  BigCircle bc2_24(g2[24], p2[24], g[7], p[7], g[6], p[6]);
  BigCircle bc2_28(g2[28], p2[28], g[9], p[9], g[8], p[8]);
  BigCircle bc2_35(g2[35], p2[35], g[13], p[13], g[12], p[12]);

  wire [37:17] g3, p3;
  BigCircle bc3_17(g3[17], p3[17], g[2], p[2], g2[16], p2[16]);
  BigCircle bc3_19(g3[19], p3[19], g2[18], p2[18], g2[16], p2[16]);
  BigCircle bc3_25(g3[25], p3[25], g2[24], p2[24], g2[21], p2[21]);
  BigCircle bc3_30(g3[30], p3[30], g[10], p[10], g2[28], p2[28]);
  BigCircle bc3_37(g3[37], p3[37], g[14], p[14], g2[35], p2[35]);

  wire [32:20] g4, p4;
  BigCircle bc4_20(g4[20], p4[20], g[4], p[4], g3[19], p3[19]);
  BigCircle bc4_22(g4[22], p4[22], g2[21], p2[21], g3[19], p3[19]);
  BigCircle bc4_26(g4[26], p4[26], g3[25], p3[25], g3[19], p3[19]);
  BigCircle bc4_32(g4[32], p4[32], g[11], p[11], g3[30], p3[30]);

  wire [33:23] g5, p5;
  BigCircle bc5_23(g5[23], p5[23], g[6], p[6], g4[22], p4[22]);
  BigCircle bc5_27(g5[27], p5[27], g[8], p[8], g4[26], p4[26]);
  BigCircle bc5_29(g5[29], p5[29], g2[28], p2[28], g4[26], p4[26]);
  BigCircle bc5_31(g5[31], p5[31], g3[30], p3[30], g4[26], p4[26]);
  BigCircle bc5_33(g5[33], p5[33], g4[32], p4[32], g4[26], p4[26]);

  wire [38:34] g6, p6;
  BigCircle bc6_34(g6[34], p6[34], g[12], p[12], g5[33], p5[33]);
  BigCircle bc6_36(g6[36], p6[36], g2[35], p2[35], g5[33], p5[33]);
  BigCircle bc6_38(g6[38], p6[38], g3[37], p3[37], g5[33], p5[33]);

  wire [39:39] g7, p7;
  BigCircle bc7_39(g7[39], p7[39], g[15], p[15], g6[38], p6[38]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[16]);
  SmallCircle sc2(c[2], g3[17]);
  SmallCircle sc3(c[3], g3[19]);
  SmallCircle sc4(c[4], g4[20]);
  SmallCircle sc5(c[5], g4[22]);
  SmallCircle sc6(c[6], g5[23]);
  SmallCircle sc7(c[7], g4[26]);
  SmallCircle sc8(c[8], g5[27]);
  SmallCircle sc9(c[9], g5[29]);
  SmallCircle sc10(c[10], g5[31]);
  SmallCircle sc11(c[11], g5[33]);
  SmallCircle sc12(c[12], g6[34]);
  SmallCircle sc13(c[13], g6[36]);
  SmallCircle sc14(c[14], g6[38]);
  SmallCircle sc15(c[15], g7[39]);
  Triangle tr0(sum[0], p[0], cin);
  Triangle tr1(sum[1], p[1], c[0]);
  Triangle tr2(sum[2], p[2], c[1]);
  Triangle tr3(sum[3], p[3], c[2]);
  Triangle tr4(sum[4], p[4], c[3]);
  Triangle tr5(sum[5], p[5], c[4]);
  Triangle tr6(sum[6], p[6], c[5]);
  Triangle tr7(sum[7], p[7], c[6]);
  Triangle tr8(sum[8], p[8], c[7]);
  Triangle tr9(sum[9], p[9], c[8]);
  Triangle tr10(sum[10], p[10], c[9]);
  Triangle tr11(sum[11], p[11], c[10]);
  Triangle tr12(sum[12], p[12], c[11]);
  Triangle tr13(sum[13], p[13], c[12]);
  Triangle tr14(sum[14], p[14], c[13]);
  Triangle tr15(sum[15], p[15], c[14]);

  buf (cout, c[15]);

endmodule