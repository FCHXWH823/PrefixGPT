
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


module GPTPrefix16_L5(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [27:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_17(g2[17], p2[17], g[3], p[3], g[2], p[2]);
  BigCircle bc2_19(g2[19], p2[19], g[5], p[5], g[4], p[4]);
  BigCircle bc2_20(g2[20], p2[20], g[7], p[7], g[6], p[6]);
  BigCircle bc2_23(g2[23], p2[23], g[9], p[9], g[8], p[8]);
  BigCircle bc2_24(g2[24], p2[24], g[11], p[11], g[10], p[10]);
  BigCircle bc2_26(g2[26], p2[26], g[13], p[13], g[12], p[12]);
  BigCircle bc2_27(g2[27], p2[27], g[15], p[15], g[14], p[14]);

  wire [43:18] g3, p3;
  BigCircle bc3_18(g3[18], p3[18], g2[17], p2[17], g2[16], p2[16]);
  BigCircle bc3_21(g3[21], p3[21], g2[20], p2[20], g2[19], p2[19]);
  BigCircle bc3_25(g3[25], p3[25], g2[24], p2[24], g2[23], p2[23]);
  BigCircle bc3_28(g3[28], p3[28], g2[27], p2[27], g2[26], p2[26]);
  BigCircle bc3_31(g3[31], p3[31], g[2], p[2], g2[16], p2[16]);
  BigCircle bc3_35(g3[35], p3[35], g[10], p[10], g2[23], p2[23]);
  BigCircle bc3_43(g3[43], p3[43], g[14], p[14], g2[26], p2[26]);

  wire [44:22] g4, p4;
  BigCircle bc4_22(g4[22], p4[22], g3[21], p3[21], g3[18], p3[18]);
  BigCircle bc4_29(g4[29], p4[29], g3[28], p3[28], g3[25], p3[25]);
  BigCircle bc4_32(g4[32], p4[32], g[4], p[4], g3[18], p3[18]);
  BigCircle bc4_36(g4[36], p4[36], g2[19], p2[19], g3[18], p3[18]);
  BigCircle bc4_40(g4[40], p4[40], g[12], p[12], g3[25], p3[25]);
  BigCircle bc4_41(g4[41], p4[41], g2[26], p2[26], g3[25], p3[25]);
  BigCircle bc4_44(g4[44], p4[44], g3[43], p3[43], g3[25], p3[25]);

  wire [46:30] g5, p5;
  BigCircle bc5_30(g5[30], p5[30], g4[29], p4[29], g4[22], p4[22]);
  BigCircle bc5_33(g5[33], p5[33], g[8], p[8], g4[22], p4[22]);
  BigCircle bc5_34(g5[34], p5[34], g2[23], p2[23], g4[22], p4[22]);
  BigCircle bc5_37(g5[37], p5[37], g[6], p[6], g4[36], p4[36]);
  BigCircle bc5_38(g5[38], p5[38], g3[35], p3[35], g4[22], p4[22]);
  BigCircle bc5_39(g5[39], p5[39], g3[25], p3[25], g4[22], p4[22]);
  BigCircle bc5_42(g5[42], p5[42], g4[41], p4[41], g4[22], p4[22]);
  BigCircle bc5_45(g5[45], p5[45], g4[40], p4[40], g4[22], p4[22]);
  BigCircle bc5_46(g5[46], p5[46], g4[44], p4[44], g4[22], p4[22]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[16]);
  SmallCircle sc2(c[2], g3[31]);
  SmallCircle sc3(c[3], g3[18]);
  SmallCircle sc4(c[4], g4[32]);
  SmallCircle sc5(c[5], g4[36]);
  SmallCircle sc6(c[6], g5[37]);
  SmallCircle sc7(c[7], g4[22]);
  SmallCircle sc8(c[8], g5[33]);
  SmallCircle sc9(c[9], g5[34]);
  SmallCircle sc10(c[10], g5[38]);
  SmallCircle sc11(c[11], g5[39]);
  SmallCircle sc12(c[12], g5[45]);
  SmallCircle sc13(c[13], g5[42]);
  SmallCircle sc14(c[14], g5[46]);
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