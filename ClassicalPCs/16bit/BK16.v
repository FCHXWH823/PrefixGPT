
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


module BK16(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [38:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_18(g2[18], p2[18], g[3], p[3], g[2], p[2]);
  BigCircle bc2_21(g2[21], p2[21], g[5], p[5], g[4], p[4]);
  BigCircle bc2_24(g2[24], p2[24], g[7], p[7], g[6], p[6]);
  BigCircle bc2_28(g2[28], p2[28], g[9], p[9], g[8], p[8]);
  BigCircle bc2_31(g2[31], p2[31], g[11], p[11], g[10], p[10]);
  BigCircle bc2_35(g2[35], p2[35], g[13], p[13], g[12], p[12]);
  BigCircle bc2_38(g2[38], p2[38], g[15], p[15], g[14], p[14]);

  wire [39:17] g3, p3;
  BigCircle bc3_17(g3[17], p3[17], g[2], p[2], g2[16], p2[16]);
  BigCircle bc3_19(g3[19], p3[19], g2[18], p2[18], g2[16], p2[16]);
  BigCircle bc3_25(g3[25], p3[25], g2[24], p2[24], g2[21], p2[21]);
  BigCircle bc3_32(g3[32], p3[32], g2[31], p2[31], g2[28], p2[28]);
  BigCircle bc3_39(g3[39], p3[39], g2[38], p2[38], g2[35], p2[35]);

  wire [40:20] g4, p4;
  BigCircle bc4_20(g4[20], p4[20], g[4], p[4], g3[19], p3[19]);
  BigCircle bc4_22(g4[22], p4[22], g2[21], p2[21], g3[19], p3[19]);
  BigCircle bc4_26(g4[26], p4[26], g3[25], p3[25], g3[19], p3[19]);
  BigCircle bc4_40(g4[40], p4[40], g3[39], p3[39], g3[32], p3[32]);

  wire [41:23] g5, p5;
  BigCircle bc5_23(g5[23], p5[23], g[6], p[6], g4[22], p4[22]);
  BigCircle bc5_27(g5[27], p5[27], g[8], p[8], g4[26], p4[26]);
  BigCircle bc5_29(g5[29], p5[29], g2[28], p2[28], g4[26], p4[26]);
  BigCircle bc5_33(g5[33], p5[33], g3[32], p3[32], g4[26], p4[26]);
  BigCircle bc5_41(g5[41], p5[41], g4[40], p4[40], g4[26], p4[26]);

  wire [36:30] g6, p6;
  BigCircle bc6_30(g6[30], p6[30], g[10], p[10], g5[29], p5[29]);
  BigCircle bc6_34(g6[34], p6[34], g[12], p[12], g5[33], p5[33]);
  BigCircle bc6_36(g6[36], p6[36], g2[35], p2[35], g5[33], p5[33]);

  wire [37:37] g7, p7;
  BigCircle bc7_37(g7[37], p7[37], g[14], p[14], g6[36], p6[36]);

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
  SmallCircle sc10(c[10], g6[30]);
  SmallCircle sc11(c[11], g5[33]);
  SmallCircle sc12(c[12], g6[34]);
  SmallCircle sc13(c[13], g6[36]);
  SmallCircle sc14(c[14], g7[37]);
  SmallCircle sc15(c[15], g5[41]);
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