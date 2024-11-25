
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


module KoggeStone16(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [30:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_17(g2[17], p2[17], g[2], p[2], g[1], p[1]);
  BigCircle bc2_18(g2[18], p2[18], g[3], p[3], g[2], p[2]);
  BigCircle bc2_19(g2[19], p2[19], g[4], p[4], g[3], p[3]);
  BigCircle bc2_20(g2[20], p2[20], g[5], p[5], g[4], p[4]);
  BigCircle bc2_21(g2[21], p2[21], g[6], p[6], g[5], p[5]);
  BigCircle bc2_22(g2[22], p2[22], g[7], p[7], g[6], p[6]);
  BigCircle bc2_23(g2[23], p2[23], g[8], p[8], g[7], p[7]);
  BigCircle bc2_24(g2[24], p2[24], g[9], p[9], g[8], p[8]);
  BigCircle bc2_25(g2[25], p2[25], g[10], p[10], g[9], p[9]);
  BigCircle bc2_26(g2[26], p2[26], g[11], p[11], g[10], p[10]);
  BigCircle bc2_27(g2[27], p2[27], g[12], p[12], g[11], p[11]);
  BigCircle bc2_28(g2[28], p2[28], g[13], p[13], g[12], p[12]);
  BigCircle bc2_29(g2[29], p2[29], g[14], p[14], g[13], p[13]);
  BigCircle bc2_30(g2[30], p2[30], g[15], p[15], g[14], p[14]);

  wire [44:31] g3, p3;
  BigCircle bc3_31(g3[31], p3[31], g2[17], p2[17], g[0], p[0]);
  BigCircle bc3_32(g3[32], p3[32], g2[18], p2[18], g2[16], p2[16]);
  BigCircle bc3_33(g3[33], p3[33], g2[19], p2[19], g2[17], p2[17]);
  BigCircle bc3_34(g3[34], p3[34], g2[20], p2[20], g2[18], p2[18]);
  BigCircle bc3_35(g3[35], p3[35], g2[21], p2[21], g2[19], p2[19]);
  BigCircle bc3_36(g3[36], p3[36], g2[22], p2[22], g2[20], p2[20]);
  BigCircle bc3_37(g3[37], p3[37], g2[23], p2[23], g2[21], p2[21]);
  BigCircle bc3_38(g3[38], p3[38], g2[24], p2[24], g2[22], p2[22]);
  BigCircle bc3_39(g3[39], p3[39], g2[25], p2[25], g2[23], p2[23]);
  BigCircle bc3_40(g3[40], p3[40], g2[26], p2[26], g2[24], p2[24]);
  BigCircle bc3_41(g3[41], p3[41], g2[27], p2[27], g2[25], p2[25]);
  BigCircle bc3_42(g3[42], p3[42], g2[28], p2[28], g2[26], p2[26]);
  BigCircle bc3_43(g3[43], p3[43], g2[29], p2[29], g2[27], p2[27]);
  BigCircle bc3_44(g3[44], p3[44], g2[30], p2[30], g2[28], p2[28]);

  wire [56:45] g4, p4;
  BigCircle bc4_45(g4[45], p4[45], g3[33], p3[33], g[0], p[0]);
  BigCircle bc4_46(g4[46], p4[46], g3[34], p3[34], g2[16], p2[16]);
  BigCircle bc4_47(g4[47], p4[47], g3[35], p3[35], g3[31], p3[31]);
  BigCircle bc4_48(g4[48], p4[48], g3[36], p3[36], g3[32], p3[32]);
  BigCircle bc4_49(g4[49], p4[49], g3[37], p3[37], g3[33], p3[33]);
  BigCircle bc4_50(g4[50], p4[50], g3[38], p3[38], g3[34], p3[34]);
  BigCircle bc4_51(g4[51], p4[51], g3[39], p3[39], g3[35], p3[35]);
  BigCircle bc4_52(g4[52], p4[52], g3[40], p3[40], g3[36], p3[36]);
  BigCircle bc4_53(g4[53], p4[53], g3[41], p3[41], g3[37], p3[37]);
  BigCircle bc4_54(g4[54], p4[54], g3[42], p3[42], g3[38], p3[38]);
  BigCircle bc4_55(g4[55], p4[55], g3[43], p3[43], g3[39], p3[39]);
  BigCircle bc4_56(g4[56], p4[56], g3[44], p3[44], g3[40], p3[40]);

  wire [64:57] g5, p5;
  BigCircle bc5_57(g5[57], p5[57], g4[49], p4[49], g[0], p[0]);
  BigCircle bc5_58(g5[58], p5[58], g4[50], p4[50], g2[16], p2[16]);
  BigCircle bc5_59(g5[59], p5[59], g4[51], p4[51], g3[31], p3[31]);
  BigCircle bc5_60(g5[60], p5[60], g4[52], p4[52], g3[32], p3[32]);
  BigCircle bc5_61(g5[61], p5[61], g4[53], p4[53], g4[45], p4[45]);
  BigCircle bc5_62(g5[62], p5[62], g4[54], p4[54], g4[46], p4[46]);
  BigCircle bc5_63(g5[63], p5[63], g4[55], p4[55], g4[47], p4[47]);
  BigCircle bc5_64(g5[64], p5[64], g4[56], p4[56], g4[48], p4[48]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[16]);
  SmallCircle sc2(c[2], g3[31]);
  SmallCircle sc3(c[3], g3[32]);
  SmallCircle sc4(c[4], g4[45]);
  SmallCircle sc5(c[5], g4[46]);
  SmallCircle sc6(c[6], g4[47]);
  SmallCircle sc7(c[7], g4[48]);
  SmallCircle sc8(c[8], g5[57]);
  SmallCircle sc9(c[9], g5[58]);
  SmallCircle sc10(c[10], g5[59]);
  SmallCircle sc11(c[11], g5[60]);
  SmallCircle sc12(c[12], g5[61]);
  SmallCircle sc13(c[13], g5[62]);
  SmallCircle sc14(c[14], g5[63]);
  SmallCircle sc15(c[15], g5[64]);
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