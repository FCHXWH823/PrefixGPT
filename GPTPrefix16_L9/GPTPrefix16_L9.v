
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


module GPTPrefix16_L9(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [31:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_24(g2[24], p2[24], g[6], p[6], g[5], p[5]);
  BigCircle bc2_26(g2[26], p2[26], g[9], p[9], g[8], p[8]);
  BigCircle bc2_31(g2[31], p2[31], g[13], p[13], g[12], p[12]);

  wire [34:17] g3, p3;
  BigCircle bc3_17(g3[17], p3[17], g[2], p[2], g2[16], p2[16]);
  BigCircle bc3_25(g3[25], p3[25], g[7], p[7], g2[24], p2[24]);
  BigCircle bc3_34(g3[34], p3[34], g[14], p[14], g2[31], p2[31]);

  wire [35:18] g4, p4;
  BigCircle bc4_18(g4[18], p4[18], g[3], p[3], g3[17], p3[17]);
  BigCircle bc4_27(g4[27], p4[27], g2[26], p2[26], g3[25], p3[25]);
  BigCircle bc4_35(g4[35], p4[35], g[15], p[15], g3[34], p3[34]);

  wire [19:19] g5, p5;
  BigCircle bc5_19(g5[19], p5[19], g[4], p[4], g4[18], p4[18]);

  wire [28:20] g6, p6;
  BigCircle bc6_20(g6[20], p6[20], g[5], p[5], g5[19], p5[19]);
  BigCircle bc6_28(g6[28], p6[28], g4[27], p4[27], g5[19], p5[19]);

  wire [29:21] g7, p7;
  BigCircle bc7_21(g7[21], p7[21], g[6], p[6], g6[20], p6[20]);
  BigCircle bc7_29(g7[29], p7[29], g[10], p[10], g6[28], p6[28]);

  wire [30:22] g8, p8;
  BigCircle bc8_22(g8[22], p8[22], g[7], p[7], g7[21], p7[21]);
  BigCircle bc8_30(g8[30], p8[30], g[11], p[11], g7[29], p7[29]);

  wire [37:23] g9, p9;
  BigCircle bc9_23(g9[23], p9[23], g[8], p[8], g8[22], p8[22]);
  BigCircle bc9_32(g9[32], p9[32], g[12], p[12], g8[30], p8[30]);
  BigCircle bc9_33(g9[33], p9[33], g2[31], p2[31], g8[30], p8[30]);
  BigCircle bc9_36(g9[36], p9[36], g4[35], p4[35], g8[30], p8[30]);
  BigCircle bc9_37(g9[37], p9[37], g3[34], p3[34], g8[30], p8[30]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[16]);
  SmallCircle sc2(c[2], g3[17]);
  SmallCircle sc3(c[3], g4[18]);
  SmallCircle sc4(c[4], g5[19]);
  SmallCircle sc5(c[5], g6[20]);
  SmallCircle sc6(c[6], g7[21]);
  SmallCircle sc7(c[7], g8[22]);
  SmallCircle sc8(c[8], g9[23]);
  SmallCircle sc9(c[9], g6[28]);
  SmallCircle sc10(c[10], g7[29]);
  SmallCircle sc11(c[11], g8[30]);
  SmallCircle sc12(c[12], g9[32]);
  SmallCircle sc13(c[13], g9[33]);
  SmallCircle sc14(c[14], g9[37]);
  SmallCircle sc15(c[15], g9[36]);
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