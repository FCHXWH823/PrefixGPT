
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


module SK16(output [15:0] sum, output cout, input [15:0] a, b);

  wire cin = 1'b0;
  wire [15:0] c;
  wire [15:0] g, p;
  Square sq[15:0](g, p, a, b);

  wire [44:16] g2, p2;
  BigCircle bc2_16(g2[16], p2[16], g[1], p[1], g[0], p[0]);
  BigCircle bc2_18(g2[18], p2[18], g[3], p[3], g[2], p[2]);
  BigCircle bc2_21(g2[21], p2[21], g[5], p[5], g[4], p[4]);
  BigCircle bc2_25(g2[25], p2[25], g[7], p[7], g[6], p[6]);
  BigCircle bc2_29(g2[29], p2[29], g[9], p[9], g[8], p[8]);
  BigCircle bc2_33(g2[33], p2[33], g[11], p[11], g[10], p[10]);
  BigCircle bc2_38(g2[38], p2[38], g[13], p[13], g[12], p[12]);
  BigCircle bc2_44(g2[44], p2[44], g[15], p[15], g[14], p[14]);

  wire [45:17] g3, p3;
  BigCircle bc3_17(g3[17], p3[17], g[2], p[2], g2[16], p2[16]);
  BigCircle bc3_19(g3[19], p3[19], g2[18], p2[18], g2[16], p2[16]);
  BigCircle bc3_23(g3[23], p3[23], g[6], p[6], g2[21], p2[21]);
  BigCircle bc3_26(g3[26], p3[26], g2[25], p2[25], g2[21], p2[21]);
  BigCircle bc3_31(g3[31], p3[31], g[10], p[10], g2[29], p2[29]);
  BigCircle bc3_34(g3[34], p3[34], g2[33], p2[33], g2[29], p2[29]);
  BigCircle bc3_41(g3[41], p3[41], g[14], p[14], g2[38], p2[38]);
  BigCircle bc3_45(g3[45], p3[45], g2[44], p2[44], g2[38], p2[38]);

  wire [46:20] g4, p4;
  BigCircle bc4_20(g4[20], p4[20], g[4], p[4], g3[19], p3[19]);
  BigCircle bc4_22(g4[22], p4[22], g2[21], p2[21], g3[19], p3[19]);
  BigCircle bc4_24(g4[24], p4[24], g3[23], p3[23], g3[19], p3[19]);
  BigCircle bc4_27(g4[27], p4[27], g3[26], p3[26], g3[19], p3[19]);
  BigCircle bc4_36(g4[36], p4[36], g[12], p[12], g3[34], p3[34]);
  BigCircle bc4_39(g4[39], p4[39], g2[38], p2[38], g3[34], p3[34]);
  BigCircle bc4_42(g4[42], p4[42], g3[41], p3[41], g3[34], p3[34]);
  BigCircle bc4_46(g4[46], p4[46], g3[45], p3[45], g3[34], p3[34]);

  wire [47:28] g5, p5;
  BigCircle bc5_28(g5[28], p5[28], g[8], p[8], g4[27], p4[27]);
  BigCircle bc5_30(g5[30], p5[30], g2[29], p2[29], g4[27], p4[27]);
  BigCircle bc5_32(g5[32], p5[32], g3[31], p3[31], g4[27], p4[27]);
  BigCircle bc5_35(g5[35], p5[35], g3[34], p3[34], g4[27], p4[27]);
  BigCircle bc5_37(g5[37], p5[37], g4[36], p4[36], g4[27], p4[27]);
  BigCircle bc5_40(g5[40], p5[40], g4[39], p4[39], g4[27], p4[27]);
  BigCircle bc5_43(g5[43], p5[43], g4[42], p4[42], g4[27], p4[27]);
  BigCircle bc5_47(g5[47], p5[47], g4[46], p4[46], g4[27], p4[27]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[16]);
  SmallCircle sc2(c[2], g3[17]);
  SmallCircle sc3(c[3], g3[19]);
  SmallCircle sc4(c[4], g4[20]);
  SmallCircle sc5(c[5], g4[22]);
  SmallCircle sc6(c[6], g4[24]);
  SmallCircle sc7(c[7], g4[27]);
  SmallCircle sc8(c[8], g5[28]);
  SmallCircle sc9(c[9], g5[30]);
  SmallCircle sc10(c[10], g5[32]);
  SmallCircle sc11(c[11], g5[35]);
  SmallCircle sc12(c[12], g5[37]);
  SmallCircle sc13(c[13], g5[40]);
  SmallCircle sc14(c[14], g5[43]);
  SmallCircle sc15(c[15], g5[47]);
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