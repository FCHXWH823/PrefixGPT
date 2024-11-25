
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


module GPTPrefix16_L8(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [30:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_23(g2[23], p2[23], g[6], p[6], g[5], p[5]);
  BigCircle bc2_27(g2[27], p2[27], g[10], p[10], g[9], p[9]);
  BigCircle bc2_30(g2[30], p2[30], g[13], p[13], g[12], p[12]);

  wire [31:17] g3, p3;
  BigCircle bc3_17(g3[17], p3[17], g[2], p[2], g2[16], p2[16]);
  BigCircle bc3_24(g3[24], p3[24], g[7], p[7], g2[23], p2[23]);
  BigCircle bc3_28(g3[28], p3[28], g[11], p[11], g2[27], p2[27]);
  BigCircle bc3_31(g3[31], p3[31], g[14], p[14], g2[30], p2[30]);

  wire [32:18] g4, p4;
  BigCircle bc4_18(g4[18], p4[18], g[3], p[3], g3[17], p3[17]);
  BigCircle bc4_25(g4[25], p4[25], g[8], p[8], g3[24], p3[24]);
  BigCircle bc4_32(g4[32], p4[32], g[15], p[15], g3[31], p3[31]);

  wire [19:19] g5, p5;
  BigCircle bc5_19(g5[19], p5[19], g[4], p[4], g4[18], p4[18]);

  wire [26:20] g6, p6;
  BigCircle bc6_20(g6[20], p6[20], g[5], p[5], g5[19], p5[19]);
  BigCircle bc6_26(g6[26], p6[26], g4[25], p4[25], g5[19], p5[19]);

  wire [34:21] g7, p7;
  BigCircle bc7_21(g7[21], p7[21], g[6], p[6], g6[20], p6[20]);
  BigCircle bc7_29(g7[29], p7[29], g3[28], p3[28], g6[26], p6[26]);
  BigCircle bc7_34(g7[34], p7[34], g[9], p[9], g6[26], p6[26]);

  wire [38:22] g8, p8;
  BigCircle bc8_22(g8[22], p8[22], g[7], p[7], g7[21], p7[21]);
  BigCircle bc8_33(g8[33], p8[33], g4[32], p4[32], g7[29], p7[29]);
  BigCircle bc8_35(g8[35], p8[35], g[10], p[10], g7[34], p7[34]);
  BigCircle bc8_36(g8[36], p8[36], g[12], p[12], g7[29], p7[29]);
  BigCircle bc8_37(g8[37], p8[37], g2[30], p2[30], g7[29], p7[29]);
  BigCircle bc8_38(g8[38], p8[38], g3[31], p3[31], g7[29], p7[29]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[16]);
  SmallCircle sc2(c[2], g3[17]);
  SmallCircle sc3(c[3], g4[18]);
  SmallCircle sc4(c[4], g5[19]);
  SmallCircle sc5(c[5], g6[20]);
  SmallCircle sc6(c[6], g7[21]);
  SmallCircle sc7(c[7], g8[22]);
  SmallCircle sc8(c[8], g6[26]);
  SmallCircle sc9(c[9], g7[34]);
  SmallCircle sc10(c[10], g8[35]);
  SmallCircle sc11(c[11], g7[29]);
  SmallCircle sc12(c[12], g8[36]);
  SmallCircle sc13(c[13], g8[37]);
  SmallCircle sc14(c[14], g8[38]);
  SmallCircle sc15(c[15], g8[33]);
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