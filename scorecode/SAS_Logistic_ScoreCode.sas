   /*---------------------------------------------------------
     Generated SAS Scoring Code
     Date: 19Apr2026:17:55:45
     -------------------------------------------------------*/

   drop _badval_ _linp_ _temp_ _i_ _j_;
   _badval_ = 0;
   _linp_   = 0;
   _temp_   = 0;
   _i_      = 0;
   _j_      = 0;
   drop MACLOGBIG;
   MACLOGBIG= 7.0978271289338392e+02;

   array _xrow_12649311_0_{68} _temporary_;
   array _beta_12649311_0_{68} _temporary_ (    0.28211236332273
            0.0037132029453
           -2.6383634446473
          -2.52881527031206
           -2.3028409849228
          -1.94560688095355
          -1.77183421371652
          -1.38566597545734
          -1.10337964041915
          -0.91159976978443
          -0.74241817971931
          -0.61121056971558
          -0.39727090593462
          -0.24434108198954
                          0
           0.08992989923691
                          0
          -0.13756391753117
                          0
           -0.5168778196041
                          0
           1.35935020701951
           1.14763474424336
           0.75824854705743
              0.30836477982
                          0
          -0.13605606152896
                          0
          -0.26925791083952
                          0
           -0.0821420436569
                          0
          -0.44133952768202
          -0.32193427735172
                          0
          -0.37630781220518
                          0
          -1.01061249426107
                          0
           0.36924008991287
           0.12057861154186
           0.03812745425605
                          0
          -0.32602742540056
          -0.01901475170535
           0.15655180705523
           0.01609747600908
                          0
          -0.45533615460615
          -0.33596189573737
          -0.16968261826447
                          0
           0.27848566723566
           0.15526323318749
          -0.01985446762479
          -0.10665099756835
          -0.22555287000567
          -0.17083518365903
           -0.1616355755541
          -0.01525232378484
           0.11487265048018
                          0
          -0.33750882283976
          -0.15331719278091
           0.01538129474561
                          0
          -0.76356876389196
                          0);

   length _IMP_AgeCategory_ $2; drop _IMP_AgeCategory_;
   _IMP_AgeCategory_ = left(trim(put(IMP_AgeCategory,BEST2.)));
   length _Sex_ $1; drop _Sex_;
   _Sex_ = left(trim(put(Sex,BEST1.)));
   length _IMP_AlcoholDrinkers_ $1; drop _IMP_AlcoholDrinkers_;
   _IMP_AlcoholDrinkers_ = left(trim(put(IMP_AlcoholDrinkers,BEST1.)));
   length _IMP_BlindOrVisionDifficulty_ $1; drop _IMP_BlindOrVisionDifficulty_;
   _IMP_BlindOrVisionDifficulty_ = left(trim(put(IMP_BlindOrVisionDifficulty,BEST1.)));
   length _IMP_HadDepressiveDisorder_ $1; drop _IMP_HadDepressiveDisorder_;
   _IMP_HadDepressiveDisorder_ = left(trim(put(IMP_HadDepressiveDisorder,BEST1.)));
   length _IMP_RaceEthnicityCategory_ $29; drop _IMP_RaceEthnicityCategory_;
   _IMP_RaceEthnicityCategory_ = left(trim(put(IMP_RaceEthnicityCategory,$29.)));
   length _IMP_HadDiabetes_ $1; drop _IMP_HadDiabetes_;
   _IMP_HadDiabetes_ = left(trim(put(IMP_HadDiabetes,BEST1.)));
   length _IMP_HadStroke_ $1; drop _IMP_HadStroke_;
   _IMP_HadStroke_ = left(trim(put(IMP_HadStroke,BEST1.)));
   length _IMP_RemovedTeeth_ $1; drop _IMP_RemovedTeeth_;
   _IMP_RemovedTeeth_ = left(trim(put(IMP_RemovedTeeth,$1.)));
   length _IMP_LastCheckupTime_ $1; drop _IMP_LastCheckupTime_;
   _IMP_LastCheckupTime_ = left(trim(put(IMP_LastCheckupTime,BEST1.)));
   length _IMP_SleepHours_ $2; drop _IMP_SleepHours_;
   _IMP_SleepHours_ = left(trim(put(IMP_SleepHours,BEST2.)));
   length _IMP_ChestScan_ $1; drop _IMP_ChestScan_;
   _IMP_ChestScan_ = left(trim(put(IMP_ChestScan,BEST1.)));
   length _IMP_HadCOPD_ $1; drop _IMP_HadCOPD_;
   _IMP_HadCOPD_ = left(trim(put(IMP_HadCOPD,BEST1.)));
   length _IMP_HadKidneyDisease_ $1; drop _IMP_HadKidneyDisease_;
   _IMP_HadKidneyDisease_ = left(trim(put(IMP_HadKidneyDisease,BEST1.)));
   length _IMP_SmokerStatus_ $1; drop _IMP_SmokerStatus_;
   _IMP_SmokerStatus_ = left(trim(put(IMP_SmokerStatus,BEST1.)));
   length _IMP_HadArthritis_ $1; drop _IMP_HadArthritis_;
   _IMP_HadArthritis_ = left(trim(put(IMP_HadArthritis,BEST1.)));
   length _IMP_GeneralHealth_ $1; drop _IMP_GeneralHealth_;
   _IMP_GeneralHealth_ = left(trim(put(IMP_GeneralHealth,BEST1.)));
   if missing(IMP_PhysicalHealthDays)
      then do;
         _badval_ = 1;
         goto skip_12649311_0;
   end;

   do _i_=1 to 68; _xrow_12649311_0_{_i_} = 0; end;

   _xrow_12649311_0_[1] = 1;

   _xrow_12649311_0_[2] = IMP_PhysicalHealthDays;

   _temp_ = 1;
   select (_IMP_AgeCategory_);
      when ('1') _xrow_12649311_0_[3] = _temp_;
      when ('2') _xrow_12649311_0_[4] = _temp_;
      when ('3') _xrow_12649311_0_[5] = _temp_;
      when ('4') _xrow_12649311_0_[6] = _temp_;
      when ('5') _xrow_12649311_0_[7] = _temp_;
      when ('6') _xrow_12649311_0_[8] = _temp_;
      when ('7') _xrow_12649311_0_[9] = _temp_;
      when ('8') _xrow_12649311_0_[10] = _temp_;
      when ('9') _xrow_12649311_0_[11] = _temp_;
      when ('10') _xrow_12649311_0_[12] = _temp_;
      when ('11') _xrow_12649311_0_[13] = _temp_;
      when ('12') _xrow_12649311_0_[14] = _temp_;
      when ('13') _xrow_12649311_0_[15] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_AlcoholDrinkers_);
      when ('0') _xrow_12649311_0_[16] = _temp_;
      when ('1') _xrow_12649311_0_[17] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_BlindOrVisionDifficulty_);
      when ('0') _xrow_12649311_0_[18] = _temp_;
      when ('1') _xrow_12649311_0_[19] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_ChestScan_);
      when ('0') _xrow_12649311_0_[20] = _temp_;
      when ('1') _xrow_12649311_0_[21] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_GeneralHealth_);
      when ('1') _xrow_12649311_0_[22] = _temp_;
      when ('2') _xrow_12649311_0_[23] = _temp_;
      when ('3') _xrow_12649311_0_[24] = _temp_;
      when ('4') _xrow_12649311_0_[25] = _temp_;
      when ('5') _xrow_12649311_0_[26] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_HadArthritis_);
      when ('0') _xrow_12649311_0_[27] = _temp_;
      when ('1') _xrow_12649311_0_[28] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_HadCOPD_);
      when ('0') _xrow_12649311_0_[29] = _temp_;
      when ('1') _xrow_12649311_0_[30] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_HadDepressiveDisorder_);
      when ('0') _xrow_12649311_0_[31] = _temp_;
      when ('1') _xrow_12649311_0_[32] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_HadDiabetes_);
      when ('0') _xrow_12649311_0_[33] = _temp_;
      when ('1') _xrow_12649311_0_[34] = _temp_;
      when ('2') _xrow_12649311_0_[35] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_HadKidneyDisease_);
      when ('0') _xrow_12649311_0_[36] = _temp_;
      when ('1') _xrow_12649311_0_[37] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_HadStroke_);
      when ('0') _xrow_12649311_0_[38] = _temp_;
      when ('1') _xrow_12649311_0_[39] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_LastCheckupTime_);
      when ('1') _xrow_12649311_0_[40] = _temp_;
      when ('2') _xrow_12649311_0_[41] = _temp_;
      when ('3') _xrow_12649311_0_[42] = _temp_;
      when ('4') _xrow_12649311_0_[43] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_RaceEthnicityCategory_);
      when ('Black only, Non-Hispanic') _xrow_12649311_0_[44] = _temp_;
      when ('Hispanic') _xrow_12649311_0_[45] = _temp_;
      when ('Multiracial, Non-Hispanic') _xrow_12649311_0_[46] = _temp_;
      when ('Other race only, Non-Hispanic') _xrow_12649311_0_[47] = _temp_;
      when ('White only, Non-Hispanic') _xrow_12649311_0_[48] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_RemovedTeeth_);
      when ('0') _xrow_12649311_0_[49] = _temp_;
      when ('1') _xrow_12649311_0_[50] = _temp_;
      when ('2') _xrow_12649311_0_[51] = _temp_;
      when ('3') _xrow_12649311_0_[52] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_SleepHours_);
      when ('3') _xrow_12649311_0_[53] = _temp_;
      when ('4') _xrow_12649311_0_[54] = _temp_;
      when ('5') _xrow_12649311_0_[55] = _temp_;
      when ('6') _xrow_12649311_0_[56] = _temp_;
      when ('7') _xrow_12649311_0_[57] = _temp_;
      when ('8') _xrow_12649311_0_[58] = _temp_;
      when ('9') _xrow_12649311_0_[59] = _temp_;
      when ('10') _xrow_12649311_0_[60] = _temp_;
      when ('11') _xrow_12649311_0_[61] = _temp_;
      when ('12') _xrow_12649311_0_[62] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_IMP_SmokerStatus_);
      when ('0') _xrow_12649311_0_[63] = _temp_;
      when ('1') _xrow_12649311_0_[64] = _temp_;
      when ('2') _xrow_12649311_0_[65] = _temp_;
      when ('3') _xrow_12649311_0_[66] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   _temp_ = 1;
   select (_Sex_);
      when ('0') _xrow_12649311_0_[67] = _temp_;
      when ('1') _xrow_12649311_0_[68] = _temp_;
      otherwise do; _badval_ = 1; goto skip_12649311_0; end;
   end;

   do _i_=1 to 68;
      _linp_ + _xrow_12649311_0_{_i_} * _beta_12649311_0_{_i_};
   end;

   skip_12649311_0:
   length I_Heart_attack $12;
   label I_Heart_attack = 'Into: Heart attack';
   array _levels_12649311_{2} $ 12 _TEMPORARY_ ('1'
   ,'0'
   );
   label P_Heart_attack1 = 'Predicted: Heart attack=1';
   if (_badval_ eq 0) and not missing(_linp_) then do;
      if (_linp_ > 0) then do;
         P_Heart_attack1 = 1 / (1+exp(-_linp_));
      end; else do;
         P_Heart_attack1 = exp(_linp_) / (1+exp(_linp_));
      end;
      P_Heart_attack0 = 1 - P_Heart_attack1;
      if P_Heart_attack1 >= 0.5                  then do;
         I_Heart_attack = _levels_12649311_{1};
      end; else do;
         I_Heart_attack = _levels_12649311_{2};
      end;
   end; else do;
      _linp_ = .;
      P_Heart_attack1 = .;
      P_Heart_attack0 = .;
      I_Heart_attack = ' ';
   end;


   *------------------------------------------------------------*;
   * Initializing missing posterior and classification variables ;
   *------------------------------------------------------------*;
   label "P_Heart_attack0"n ='Predicted: Heart attack=0';
   if "P_Heart_attack0"n = . then "P_Heart_attack0"n =0.9435742313;
   label "P_Heart_attack1"n ='Predicted: Heart attack=1';
   if "P_Heart_attack1"n = . then "P_Heart_attack1"n =0.0564257687;
   label "I_Heart_attack"n ='Into: Heart attack';
   if missing('I_Heart_attack'n) then do;
      drop _P_;
      _P_= 0.0 ;
      if 'P_Heart_attack1'n > _P_ then do;
      _P_ = 'P_Heart_attack1'n;
      'I_Heart_attack'n = '           1';
      end;
      if 'P_Heart_attack0'n > _P_ then do;
      _P_ = 'P_Heart_attack0'n;
      'I_Heart_attack'n = '           0';
      end;
   end;
