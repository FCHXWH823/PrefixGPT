
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


module adder_16b_5l(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [54:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_18(g2[18], p2[18], g[3], p[3], g[2], p[2]);
  BigCircle bc2_20(g2[20], p2[20], g[4], p[4], g[3], p[3]);
  BigCircle bc2_22(g2[22], p2[22], g[5], p[5], g[4], p[4]);
  BigCircle bc2_24(g2[24], p2[24], g[6], p[6], g[5], p[5]);
  BigCircle bc2_27(g2[27], p2[27], g[7], p[7], g[6], p[6]);
  BigCircle bc2_30(g2[30], p2[30], g[8], p[8], g[7], p[7]);
  BigCircle bc2_33(g2[33], p2[33], g[9], p[9], g[8], p[8]);
  BigCircle bc2_36(g2[36], p2[36], g[10], p[10], g[9], p[9]);
  BigCircle bc2_39(g2[39], p2[39], g[11], p[11], g[10], p[10]);
  BigCircle bc2_42(g2[42], p2[42], g[12], p[12], g[11], p[11]);
  BigCircle bc2_46(g2[46], p2[46], g[13], p[13], g[12], p[12]);
  BigCircle bc2_50(g2[50], p2[50], g[14], p[14], g[13], p[13]);
  BigCircle bc2_54(g2[54], p2[54], g[15], p[15], g[14], p[14]);

  wire [55:17] g3, p3;
  BigCircle bc3_17(g3[17], p3[17], g[2], p[2], g2[16], p2[16]);
  BigCircle bc3_19(g3[19], p3[19], g2[18], p2[18], g2[16], p2[16]);
  BigCircle bc3_25(g3[25], p3[25], g2[24], p2[24], g2[20], p2[20]);
  BigCircle bc3_28(g3[28], p3[28], g2[27], p2[27], g2[22], p2[22]);
  BigCircle bc3_31(g3[31], p3[31], g2[30], p2[30], g2[24], p2[24]);
  BigCircle bc3_34(g3[34], p3[34], g2[33], p2[33], g2[27], p2[27]);
  BigCircle bc3_37(g3[37], p3[37], g2[36], p2[36], g2[30], p2[30]);
  BigCircle bc3_40(g3[40], p3[40], g2[39], p2[39], g2[33], p2[33]);
  BigCircle bc3_43(g3[43], p3[43], g2[42], p2[42], g2[36], p2[36]);
  BigCircle bc3_47(g3[47], p3[47], g2[46], p2[46], g2[39], p2[39]);
  BigCircle bc3_51(g3[51], p3[51], g2[50], p2[50], g2[42], p2[42]);
  BigCircle bc3_55(g3[55], p3[55], g2[54], p2[54], g2[46], p2[46]);

  wire [56:21] g4, p4;
  BigCircle bc4_21(g4[21], p4[21], g2[20], p2[20], g3[17], p3[17]);
  BigCircle bc4_23(g4[23], p4[23], g2[22], p2[22], g3[19], p3[19]);
  BigCircle bc4_26(g4[26], p4[26], g3[25], p3[25], g3[17], p3[17]);
  BigCircle bc4_29(g4[29], p4[29], g3[28], p3[28], g3[19], p3[19]);
  BigCircle bc4_44(g4[44], p4[44], g3[43], p3[43], g3[31], p3[31]);
  BigCircle bc4_48(g4[48], p4[48], g3[47], p3[47], g3[34], p3[34]);
  BigCircle bc4_52(g4[52], p4[52], g3[51], p3[51], g3[37], p3[37]);
  BigCircle bc4_56(g4[56], p4[56], g3[55], p3[55], g3[40], p3[40]);

  wire [57:32] g5, p5;
  BigCircle bc5_32(g5[32], p5[32], g3[31], p3[31], g4[21], p4[21]);
  BigCircle bc5_35(g5[35], p5[35], g3[34], p3[34], g4[23], p4[23]);
  BigCircle bc5_38(g5[38], p5[38], g3[37], p3[37], g4[26], p4[26]);
  BigCircle bc5_41(g5[41], p5[41], g3[40], p3[40], g4[29], p4[29]);
  BigCircle bc5_45(g5[45], p5[45], g4[44], p4[44], g4[21], p4[21]);
  BigCircle bc5_49(g5[49], p5[49], g4[48], p4[48], g4[23], p4[23]);
  BigCircle bc5_53(g5[53], p5[53], g4[52], p4[52], g4[26], p4[26]);
  BigCircle bc5_57(g5[57], p5[57], g4[56], p4[56], g4[29], p4[29]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[16]);
  SmallCircle sc2(c[2], g3[17]);
  SmallCircle sc3(c[3], g3[19]);
  SmallCircle sc4(c[4], g4[21]);
  SmallCircle sc5(c[5], g4[23]);
  SmallCircle sc6(c[6], g4[26]);
  SmallCircle sc7(c[7], g4[29]);
  SmallCircle sc8(c[8], g5[32]);
  SmallCircle sc9(c[9], g5[35]);
  SmallCircle sc10(c[10], g5[38]);
  SmallCircle sc11(c[11], g5[41]);
  SmallCircle sc12(c[12], g5[45]);
  SmallCircle sc13(c[13], g5[49]);
  SmallCircle sc14(c[14], g5[53]);
  SmallCircle sc15(c[15], g5[57]);
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