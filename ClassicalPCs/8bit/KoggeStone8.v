
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


module KoggeStone8(output [7:0] sum, output cout, input [7:0] a, b);

  wire cin = 1'b0;
  wire [7:0] c;
  wire [7:0] g, p;
  Square sq[7:0](g, p, a, b);

  wire [14:8] g2, p2;
  BigCircle bc2_8(g2[8], p2[8], g[1], p[1], g[0], p[0]);
  BigCircle bc2_9(g2[9], p2[9], g[2], p[2], g[1], p[1]);
  BigCircle bc2_10(g2[10], p2[10], g[3], p[3], g[2], p[2]);
  BigCircle bc2_11(g2[11], p2[11], g[4], p[4], g[3], p[3]);
  BigCircle bc2_12(g2[12], p2[12], g[5], p[5], g[4], p[4]);
  BigCircle bc2_13(g2[13], p2[13], g[6], p[6], g[5], p[5]);
  BigCircle bc2_14(g2[14], p2[14], g[7], p[7], g[6], p[6]);

  wire [20:15] g3, p3;
  BigCircle bc3_15(g3[15], p3[15], g2[9], p2[9], g[0], p[0]);
  BigCircle bc3_16(g3[16], p3[16], g2[10], p2[10], g2[8], p2[8]);
  BigCircle bc3_17(g3[17], p3[17], g2[11], p2[11], g2[9], p2[9]);
  BigCircle bc3_18(g3[18], p3[18], g2[12], p2[12], g2[10], p2[10]);
  BigCircle bc3_19(g3[19], p3[19], g2[13], p2[13], g2[11], p2[11]);
  BigCircle bc3_20(g3[20], p3[20], g2[14], p2[14], g2[12], p2[12]);

  wire [24:21] g4, p4;
  BigCircle bc4_21(g4[21], p4[21], g3[17], p3[17], g[0], p[0]);
  BigCircle bc4_22(g4[22], p4[22], g3[18], p3[18], g2[8], p2[8]);
  BigCircle bc4_23(g4[23], p4[23], g3[19], p3[19], g3[15], p3[15]);
  BigCircle bc4_24(g4[24], p4[24], g3[20], p3[20], g3[16], p3[16]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g2[8]);
  SmallCircle sc2(c[2], g3[15]);
  SmallCircle sc3(c[3], g3[16]);
  SmallCircle sc4(c[4], g4[21]);
  SmallCircle sc5(c[5], g4[22]);
  SmallCircle sc6(c[6], g4[23]);
  SmallCircle sc7(c[7], g4[24]);
  Triangle tr0(sum[0], p[0], cin);
  Triangle tr1(sum[1], p[1], c[0]);
  Triangle tr2(sum[2], p[2], c[1]);
  Triangle tr3(sum[3], p[3], c[2]);
  Triangle tr4(sum[4], p[4], c[3]);
  Triangle tr5(sum[5], p[5], c[4]);
  Triangle tr6(sum[6], p[6], c[5]);
  Triangle tr7(sum[7], p[7], c[6]);

  buf (cout, c[7]);

endmodule