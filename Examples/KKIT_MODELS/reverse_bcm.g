//genesis
// kkit Version 11 flat dumpfile
 
// Saved on Sun Aug 16 14:33:05 2020
 
include kkit {argv 1}
 
FASTDT = 1e-06
SIMDT = 0.001
CONTROLDT = 5
PLOTDT = 1
MAXTIME = 100
TRANSIENT_TIME = 2
VARIABLE_DT_FLAG = 1
DEFAULT_VOL = 1.6667e-18
VERSION = 11.0
setfield /file/modpath value /home2/bhalla/scripts/modules
kparms
 
//genesis

initdump -version 3 -ignoreorphans 1
simobjdump doqcsinfo filename accessname accesstype transcriber developer \
  citation species tissue cellcompartment methodology sources \
  model_implementation model_validation x y z
simobjdump table input output alloced step_mode stepsize x y z
simobjdump xtree path script namemode sizescale
simobjdump xcoredraw xmin xmax ymin ymax
simobjdump xtext editable
simobjdump xgraph xmin xmax ymin ymax overlay
simobjdump xplot pixflags script fg ysquish do_slope wy
simobjdump group xtree_fg_req xtree_textfg_req plotfield expanded movealone \
  link savename file version md5sum mod_save_flag x y z
simobjdump geometry size dim shape outside xtree_fg_req xtree_textfg_req x y \
  z
simobjdump kpool DiffConst CoInit Co n nInit mwt nMin vol slave_enable \
  geomname xtree_fg_req xtree_textfg_req x y z
simobjdump kreac kf kb notes xtree_fg_req xtree_textfg_req x y z
simobjdump kenz CoComplexInit CoComplex nComplexInit nComplex vol k1 k2 k3 \
  keepconc usecomplex notes xtree_fg_req xtree_textfg_req link x y z
simobjdump stim level1 width1 delay1 level2 width2 delay2 baselevel trig_time \
  trig_mode notes xtree_fg_req xtree_textfg_req is_running x y z
simobjdump xtab input output alloced step_mode stepsize notes editfunc \
  xtree_fg_req xtree_textfg_req baselevel last_x last_y is_running x y z
simobjdump kchan perm gmax Vm is_active use_nernst notes xtree_fg_req \
  xtree_textfg_req x y z
simobjdump transport input output alloced step_mode stepsize dt delay clock \
  kf xtree_fg_req xtree_textfg_req x y z
simobjdump proto x y z
simobjdump text str
simundump geometry /kinetics/geometry 0 1.6667e-18 3 sphere "" white black 0 \
  0 0
simundump geometry /kinetics/geometry[1] 0 1.6667e-18 3 sphere "" white black \
  0 0 0
simundump geometry /kinetics/geometry[2] 0 1.6667e-18 3 sphere "" white black \
  0 0 0
simundump geometry /kinetics/geometry[3] 0 1.6667e-18 3 sphere "" white black \
  0 0 0
simundump text /kinetics/notes 0 ""
call /kinetics/notes LOAD \
""
simundump text /kinetics/geometry/notes 0 ""
call /kinetics/geometry/notes LOAD \
""
simundump text /kinetics/geometry[1]/notes 0 ""
call /kinetics/geometry[1]/notes LOAD \
""
simundump text /kinetics/geometry[2]/notes 0 ""
call /kinetics/geometry[2]/notes LOAD \
""
simundump kpool /kinetics/Ca 0 0 0.08 0.08 80 80 0 0 1000 4 \
  /kinetics/geometry 62 black 0 3 0
simundump text /kinetics/Ca/notes 0 ""
call /kinetics/Ca/notes LOAD \
""
simundump kpool /kinetics/CaN 0 0 2.1 2.1 2100 2100 0 0 1000 0 \
  /kinetics/geometry 2 black -5 1 0
simundump text /kinetics/CaN/notes 0 ""
call /kinetics/CaN/notes LOAD \
""
simundump kreac /kinetics/Ca_bind_CaN 0 1e-07 0.175 "" white black -2 1 0
simundump text /kinetics/Ca_bind_CaN/notes 0 ""
call /kinetics/Ca_bind_CaN/notes LOAD \
""
simundump kreac /kinetics/Ca_bind_CaM 0 1e-12 10 "" white black 2 1 0
simundump text /kinetics/Ca_bind_CaM/notes 0 ""
call /kinetics/Ca_bind_CaM/notes LOAD \
""
simundump kpool /kinetics/Ca4.CaMKII 0 0 0 0 0 0 0 0 1000 0 \
  /kinetics/geometry 28 black 4 -1 0
simundump text /kinetics/Ca4.CaMKII/notes 0 ""
call /kinetics/Ca4.CaMKII/notes LOAD \
""
simundump kenz /kinetics/Ca4.CaMKII/kenz 0 0 0 0 0 1000 5 400 100 0 1 "" red \
  28 "" 4 -2 0
simundump text /kinetics/Ca4.CaMKII/kenz/notes 0 ""
call /kinetics/Ca4.CaMKII/kenz/notes LOAD \
""
simundump kpool /kinetics/Ca3_CaN 0 0 0 0 0 0 0 0 1000 0 /kinetics/geometry 7 \
  black -4 -1 0
simundump text /kinetics/Ca3_CaN/notes 0 ""
call /kinetics/Ca3_CaN/notes LOAD \
""
simundump kenz /kinetics/Ca3_CaN/kenz 0 0 0 0 0 1000 0.5 4000 1000 0 1 "" red \
  7 "" -4 -2 0
simundump text /kinetics/Ca3_CaN/kenz/notes 0 ""
call /kinetics/Ca3_CaN/kenz/notes LOAD \
""
simundump kpool /kinetics/CaMKII 0 0 1.15 1.15 1150 1150 0 0 1000 0 \
  /kinetics/geometry 38 black 5 1 0
simundump text /kinetics/CaMKII/notes 0 ""
call /kinetics/CaMKII/notes LOAD \
""
simundump kpool /kinetics/B1 0 0 1.52 1.52 1520 1520 0 0 1000 0 \
  /kinetics/geometry[1] 24 black 5 -3 0
simundump text /kinetics/B1/notes 0 ""
call /kinetics/B1/notes LOAD \
""
simundump kreac /kinetics/R1 0 100 35 "" white black 4 -4 0
simundump text /kinetics/R1/notes 0 ""
call /kinetics/R1/notes LOAD \
""
simundump kreac /kinetics/Activate_syn_AMPR 0 0.00112 1 "" white black 0 -6 0
simundump text /kinetics/Activate_syn_AMPR/notes 0 ""
call /kinetics/Activate_syn_AMPR/notes LOAD \
""
simundump kreac /kinetics/R2 0 100 21.6 "" white black -4 -4 0
simundump text /kinetics/R2/notes 0 ""
call /kinetics/R2/notes LOAD \
""
simundump kpool /kinetics/B3 0 0 1 1 1000 1000 0 0 1000 4 \
  /kinetics/geometry[3] 50 black -5 -3 0
simundump text /kinetics/B3/notes 0 ""
call /kinetics/B3/notes LOAD \
""
simundump text /kinetics/geometry[3]/notes 0 ""
call /kinetics/geometry[3]/notes LOAD \
""
simundump kpool /kinetics/aCaN 0 0 0 0 0 0 0 0 1000 0 /kinetics/geometry[2] \
  51 black -3 -3 0
simundump text /kinetics/aCaN/notes 0 ""
call /kinetics/aCaN/notes LOAD \
""
simundump kpool /kinetics/blocked_AMPAR 0 0 0 0 0 0 0 0 1000 0 \
  /kinetics/geometry 48 black 0 -8 0
simundump text /kinetics/blocked_AMPAR/notes 0 ""
call /kinetics/blocked_AMPAR/notes LOAD \
""
simundump kpool /kinetics/synAMPAR 0 0 0 0 0 0 0 0 1000 0 \
  /kinetics/geometry[1] 30 black 3 -3 0
simundump text /kinetics/synAMPAR/notes 0 ""
call /kinetics/synAMPAR/notes LOAD \
""
simundump xgraph /graphs/conc1 0 0 3100 0 1 0
simundump xgraph /graphs/conc2 0 0 3100 0 1.1609 0
simundump xplot /graphs/conc1/Ca.Co 3 524288 \
  "delete_plot.w <s> <d>; edit_plot.D <w>" 62 0 0 1
simundump xplot /graphs/conc1/aCaN.Co 3 524288 \
  "delete_plot.w <s> <d>; edit_plot.D <w>" 51 0 0 1
simundump xplot /graphs/conc1/Ca4.CaMKII.Co 3 524288 \
  "delete_plot.w <s> <d>; edit_plot.D <w>" 28 0 0 1
simundump xplot /graphs/conc2/synAMPAR.Co 3 524288 \
  "delete_plot.w <s> <d>; edit_plot.D <w>" 30 0 0 1
simundump xgraph /moregraphs/conc3 0 0 3100 0 1 0
simundump xgraph /moregraphs/conc4 0 0 3100 0 1 0
simundump xcoredraw /edit/draw 0 -7 7 -10 5
simundump xtree /edit/draw/tree 0 \
  /kinetics/#[],/kinetics/#[]/#[],/kinetics/#[]/#[]/#[][TYPE!=proto],/kinetics/#[]/#[]/#[][TYPE!=linkinfo]/##[] \
  "edit_elm.D <v>; drag_from_edit.w <d> <S> <x> <y> <z>" auto 0.6
simundump xtext /file/notes 0 1
addmsg /kinetics/Ca_bind_CaN /kinetics/Ca REAC A B 
addmsg /kinetics/Ca_bind_CaN /kinetics/Ca REAC A B 
addmsg /kinetics/Ca_bind_CaM /kinetics/Ca REAC A B 
addmsg /kinetics/Ca_bind_CaM /kinetics/Ca REAC A B 
addmsg /kinetics/Ca_bind_CaM /kinetics/Ca REAC A B 
addmsg /kinetics/Ca_bind_CaM /kinetics/Ca REAC A B 
addmsg /kinetics/Ca_bind_CaN /kinetics/Ca REAC A B 
addmsg /kinetics/Ca_bind_CaN /kinetics/CaN REAC A B 
addmsg /kinetics/CaN /kinetics/Ca_bind_CaN SUBSTRATE n 
addmsg /kinetics/Ca /kinetics/Ca_bind_CaN SUBSTRATE n 
addmsg /kinetics/Ca /kinetics/Ca_bind_CaN SUBSTRATE n 
addmsg /kinetics/Ca3_CaN /kinetics/Ca_bind_CaN PRODUCT n 
addmsg /kinetics/Ca /kinetics/Ca_bind_CaN SUBSTRATE n 
addmsg /kinetics/CaMKII /kinetics/Ca_bind_CaM SUBSTRATE n 
addmsg /kinetics/Ca /kinetics/Ca_bind_CaM SUBSTRATE n 
addmsg /kinetics/Ca /kinetics/Ca_bind_CaM SUBSTRATE n 
addmsg /kinetics/Ca /kinetics/Ca_bind_CaM SUBSTRATE n 
addmsg /kinetics/Ca /kinetics/Ca_bind_CaM SUBSTRATE n 
addmsg /kinetics/Ca4.CaMKII /kinetics/Ca_bind_CaM PRODUCT n 
addmsg /kinetics/Ca_bind_CaM /kinetics/Ca4.CaMKII REAC B A 
addmsg /kinetics/Ca4.CaMKII /kinetics/Ca4.CaMKII/kenz ENZYME n 
addmsg /kinetics/B1 /kinetics/Ca4.CaMKII/kenz SUBSTRATE n 
addmsg /kinetics/Ca_bind_CaN /kinetics/Ca3_CaN REAC B A 
addmsg /kinetics/Ca3_CaN /kinetics/Ca3_CaN/kenz ENZYME n 
addmsg /kinetics/B3 /kinetics/Ca3_CaN/kenz SUBSTRATE n 
addmsg /kinetics/Ca_bind_CaM /kinetics/CaMKII REAC A B 
addmsg /kinetics/Ca4.CaMKII/kenz /kinetics/B1 REAC sA B 
addmsg /kinetics/R1 /kinetics/B1 REAC B A 
addmsg /kinetics/synAMPAR /kinetics/R1 SUBSTRATE n 
addmsg /kinetics/B1 /kinetics/R1 PRODUCT n 
addmsg /kinetics/blocked_AMPAR /kinetics/Activate_syn_AMPR PRODUCT n 
addmsg /kinetics/synAMPAR /kinetics/Activate_syn_AMPR SUBSTRATE n 
addmsg /kinetics/aCaN /kinetics/Activate_syn_AMPR SUBSTRATE n 
addmsg /kinetics/aCaN /kinetics/R2 SUBSTRATE n 
addmsg /kinetics/B3 /kinetics/R2 PRODUCT n 
addmsg /kinetics/R2 /kinetics/B3 REAC B A 
addmsg /kinetics/Ca3_CaN/kenz /kinetics/B3 REAC sA B 
addmsg /kinetics/R2 /kinetics/aCaN REAC A B 
addmsg /kinetics/Ca3_CaN/kenz /kinetics/aCaN MM_PRD pA 
addmsg /kinetics/Activate_syn_AMPR /kinetics/aCaN REAC A B 
addmsg /kinetics/Activate_syn_AMPR /kinetics/blocked_AMPAR REAC B A 
addmsg /kinetics/Ca4.CaMKII/kenz /kinetics/synAMPAR MM_PRD pA 
addmsg /kinetics/R1 /kinetics/synAMPAR REAC A B 
addmsg /kinetics/Activate_syn_AMPR /kinetics/synAMPAR REAC A B 
addmsg /kinetics/Ca /graphs/conc1/Ca.Co PLOT Co *Ca.Co *62 
addmsg /kinetics/aCaN /graphs/conc1/aCaN.Co PLOT Co *aCaN.Co *51 
addmsg /kinetics/Ca4.CaMKII /graphs/conc1/Ca4.CaMKII.Co PLOT Co *Ca4.CaMKII.Co *28 
addmsg /kinetics/synAMPAR /graphs/conc2/synAMPAR.Co PLOT Co *synAMPAR.Co *30 
enddump
// End of dump

complete_loading
