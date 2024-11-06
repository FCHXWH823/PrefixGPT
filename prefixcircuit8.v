
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


module prefixcircuit8(output [7:0] sum, output cout, input [7:0] a, b);

  wire cin = 1'b0;
  wire [7:0] c;
  wire [7:0] g, p;
  Square sq[7:0](g, p, a, b);

  wire [15:8] g1, p1;
  BigCircle bc1_8(g1[8], p1[8], g[1], p[1], g[0], p[0]);
  BigCircle bc1_11(g1[11], p1[11], g[5], p[5], g[4], p[4]);
  BigCircle bc1_13(g1[13], p1[13], g[7], p[7], g[6], p[6]);
  BigCircle bc1_15(g1[15], p1[15], g[4], p[4], g[3], p[3]);

  wire [9:9] g2, p2;
  BigCircle bc2_9(g2[9], p2[9], g[2], p[2], g1[8], p1[8]);

  wire [16:10] g3, p3;
  BigCircle bc3_10(g3[10], p3[10], g[3], p[3], g2[9], p2[9]);
  BigCircle bc3_16(g3[16], p3[16], g1[15], p1[15], g2[9], p2[9]);

  wire [12:12] g4, p4;
  BigCircle bc4_12(g4[12], p4[12], g1[11], p1[11], g3[10], p3[10]);

  wire [17:14] g5, p5;
  BigCircle bc5_14(g5[14], p5[14], g1[13], p1[13], g4[12], p4[12]);
  BigCircle bc5_17(g5[17], p5[17], g[6], p[6], g4[12], p4[12]);

  SmallCircle sc0(c[0], g[0]);
  SmallCircle sc1(c[1], g1[8]);
  SmallCircle sc2(c[2], g2[9]);
  SmallCircle sc3(c[3], g3[10]);
  SmallCircle sc4(c[4], g3[16]);
  SmallCircle sc5(c[5], g4[12]);
  SmallCircle sc6(c[6], g5[17]);
  SmallCircle sc7(c[7], g5[14]);
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