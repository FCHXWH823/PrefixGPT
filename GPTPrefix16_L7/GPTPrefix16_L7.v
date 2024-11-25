
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


module GPTPrefix16_L7(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [21:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[3], p[3], g[2], p[2]);
  BigCircle bc2_17(g2[17], p2[17], g[5], p[5], g[4], p[4]);
  BigCircle bc2_18(g2[18], p2[18], g[7], p[7], g[6], p[6]);
  BigCircle bc2_19(g2[19], p2[19], g[9], p[9], g[8], p[8]);
  BigCircle bc2_20(g2[20], p2[20], g[13], p[13], g[12], p[12]);
  BigCircle bc2_21(g2[21], p2[21], g[1], p[1], g[0], p[0]);

  wire [36:22] g3, p3;
  BigCircle bc3_22(g3[22], p3[22], g[2], p[2], g2[21], p2[21]);
  BigCircle bc3_23(g3[23], p3[23], g2[16], p2[16], g2[21], p2[21]);
  BigCircle bc3_30(g3[30], p3[30], g[10], p[10], g2[19], p2[19]);
  BigCircle bc3_36(g3[36], p3[36], g[14], p[14], g2[20], p2[20]);

  wire [37:24] g4, p4;
  BigCircle bc4_24(g4[24], p4[24], g[4], p[4], g3[23], p3[23]);
  BigCircle bc4_25(g4[25], p4[25], g2[17], p2[17], g3[23], p3[23]);
  BigCircle bc4_31(g4[31], p4[31], g3[30], p3[30], g2[18], p2[18]);
  BigCircle bc4_37(g4[37], p4[37], g3[36], p3[36], g[11], p[11]);

  wire [32:26] g5, p5;
  BigCircle bc5_26(g5[26], p5[26], g[6], p[6], g4[25], p4[25]);
  BigCircle bc5_27(g5[27], p5[27], g2[18], p2[18], g4[25], p4[25]);
  BigCircle bc5_32(g5[32], p5[32], g4[31], p4[31], g4[25], p4[25]);

  wire [38:28] g6, p6;
  BigCircle bc6_28(g6[28], p6[28], g[8], p[8], g5[27], p5[27]);
  BigCircle bc6_33(g6[33], p6[33], g[11], p[11], g5[32], p5[32]);
  BigCircle bc6_38(g6[38], p6[38], g4[37], p4[37], g5[32], p5[32]);

  wire [39:29] g7, p7;
  BigCircle bc7_29(g7[29], p7[29], g[9], p[9], g6[28], p6[28]);
  BigCircle bc7_34(g7[34], p7[34], g[12], p[12], g6[33], p6[33]);
  BigCircle bc7_35(g7[35], p7[35], g2[20], p2[20], g6[33], p6[33]);
  BigCircle bc7_39(g7[39], p7[39], g[15], p[15], g6[38], p6[38]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[21]);
  SmallCircle sc2(c[2], g3[22]);
  SmallCircle sc3(c[3], g3[23]);
  SmallCircle sc4(c[4], g4[24]);
  SmallCircle sc5(c[5], g4[25]);
  SmallCircle sc6(c[6], g5[26]);
  SmallCircle sc7(c[7], g5[27]);
  SmallCircle sc8(c[8], g6[28]);
  SmallCircle sc9(c[9], g7[29]);
  SmallCircle sc10(c[10], g5[32]);
  SmallCircle sc11(c[11], g6[33]);
  SmallCircle sc12(c[12], g7[34]);
  SmallCircle sc13(c[13], g7[35]);
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