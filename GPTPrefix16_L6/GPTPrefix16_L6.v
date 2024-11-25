
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


module GPTPrefix16_L6(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [26:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_17(g2[17], p2[17], g[3], p[3], g[2], p[2]);
  BigCircle bc2_19(g2[19], p2[19], g[5], p[5], g[4], p[4]);
  BigCircle bc2_20(g2[20], p2[20], g[7], p[7], g[6], p[6]);
  BigCircle bc2_23(g2[23], p2[23], g[9], p[9], g[8], p[8]);
  BigCircle bc2_24(g2[24], p2[24], g[11], p[11], g[10], p[10]);
  BigCircle bc2_25(g2[25], p2[25], g[13], p[13], g[12], p[12]);
  BigCircle bc2_26(g2[26], p2[26], g[15], p[15], g[14], p[14]);

  wire [37:18] g3, p3;
  BigCircle bc3_18(g3[18], p3[18], g2[17], p2[17], g2[16], p2[16]);
  BigCircle bc3_21(g3[21], p3[21], g2[20], p2[20], g2[19], p2[19]);
  BigCircle bc3_27(g3[27], p3[27], g2[24], p2[24], g2[23], p2[23]);
  BigCircle bc3_28(g3[28], p3[28], g2[26], p2[26], g2[25], p2[25]);
  BigCircle bc3_31(g3[31], p3[31], g[2], p[2], g2[16], p2[16]);
  BigCircle bc3_36(g3[36], p3[36], g[10], p[10], g2[23], p2[23]);
  BigCircle bc3_37(g3[37], p3[37], g[14], p[14], g2[25], p2[25]);

  wire [32:22] g4, p4;
  BigCircle bc4_22(g4[22], p4[22], g3[21], p3[21], g3[18], p3[18]);
  BigCircle bc4_29(g4[29], p4[29], g3[28], p3[28], g3[27], p3[27]);
  BigCircle bc4_32(g4[32], p4[32], g[4], p[4], g3[18], p3[18]);

  wire [40:30] g5, p5;
  BigCircle bc5_30(g5[30], p5[30], g4[29], p4[29], g4[22], p4[22]);
  BigCircle bc5_33(g5[33], p5[33], g[5], p[5], g4[32], p4[32]);
  BigCircle bc5_35(g5[35], p5[35], g[8], p[8], g4[22], p4[22]);
  BigCircle bc5_38(g5[38], p5[38], g2[23], p2[23], g4[22], p4[22]);
  BigCircle bc5_39(g5[39], p5[39], g3[36], p3[36], g4[22], p4[22]);
  BigCircle bc5_40(g5[40], p5[40], g3[27], p3[27], g4[22], p4[22]);

  wire [43:34] g6, p6;
  BigCircle bc6_34(g6[34], p6[34], g[6], p[6], g5[33], p5[33]);
  BigCircle bc6_41(g6[41], p6[41], g[12], p[12], g5[40], p5[40]);
  BigCircle bc6_42(g6[42], p6[42], g2[25], p2[25], g5[40], p5[40]);
  BigCircle bc6_43(g6[43], p6[43], g3[37], p3[37], g5[40], p5[40]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[16]);
  SmallCircle sc2(c[2], g3[31]);
  SmallCircle sc3(c[3], g3[18]);
  SmallCircle sc4(c[4], g4[32]);
  SmallCircle sc5(c[5], g5[33]);
  SmallCircle sc6(c[6], g6[34]);
  SmallCircle sc7(c[7], g4[22]);
  SmallCircle sc8(c[8], g5[35]);
  SmallCircle sc9(c[9], g5[38]);
  SmallCircle sc10(c[10], g5[39]);
  SmallCircle sc11(c[11], g5[40]);
  SmallCircle sc12(c[12], g6[41]);
  SmallCircle sc13(c[13], g6[42]);
  SmallCircle sc14(c[14], g6[43]);
  SmallCircle sc15(c[15], g5[30]);
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