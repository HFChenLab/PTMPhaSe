// Disable corresponding elements according to the selected searching ways during window loading
if (window.addEventListener) { // Mozilla, Netscape, Firefox
    window.addEventListener('click', WindowLoad, false);
} else if (window.attachEvent) { // IE
    window.attachEvent('onload', WindowLoad);
}

function WindowLoad(event) {
    if ($('input[name=search_type]:checked').val() == 'uniprot') {
        $('#uniprot').prop('disabled', false)
        $('#gene').prop('disabled', true)
        $('#search_organism').prop('disabled', true)
    }
    else if ($('input[name=search_type]:checked').val() == 'gene') {
        $('#uniprot').prop('disabled', true)
        $('#gene').prop('disabled', false)
        $('#search_organism').prop('disabled', false)
    }
}


function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var y = document.getElementById(this.id + "autocomplete-list");
      if (y) var x = y.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
        /*y.scrollTop=0;
        y.scrollTop=$('.autocomplete-active').offset().top-y.height);*/
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        // e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}

$(document).ready(function() {
    // Change default setting of filters according to the selected prediction tools
//    $('input[name=search_table] ').change(function() {
//        if (this.value == 'RNAhybrid') {
//            $('#mfe_threshold').val('-25')
//        }
//        else if (this.value == 'IntaRNA') {
//            $('#mfe_threshold').val('-10')
//        }
//    } );


    // Change disabled status of elements according to the selected searching ways
//    $('input[name=search_type] ').change(function() {
//        if (this.value == 'trf') {
//            $('#trf').prop('disabled', false)
//            $('#gene').prop('disabled', true)
//            $('#transcript').prop('disabled', true)
//        }
//        else if (this.value == 'gene') {
//            $('#trf').prop('disabled', true)
//            $('#gene').prop('disabled', false)
//            $('#transcript').prop('disabled', true)
//        }
//        else if (this.value == 'transcript') {
//            $('#trf').prop('disabled', true)
//            $('#gene').prop('disabled', true)
//            $('#transcript').prop('disabled', false)
//        }
//    } );

    // Text field autocomplete
    var genes = ["BCR_ABL","MCRIP1","SNAP23","AIP","APBB1","CBX4","WWP2","DCTN6","EEF2K","PIK3R2","BIN1","PES1","SDCBP","DDX3X","KPNA4","CLDN4","SOCS3","ARHGAP33","DVL2","IRS4","APAF1","SLC9A3R1","TERT","CHEK1","SH2D1B","PPP1R12A","SMAD7","FYB1","MDM4","PLSCR1","TRIM24","GSTA4","NPHP1","FANCG","TP73","HDAC3","BIRC5","INSIG1","CLOCK","SOCS1","PDPK1","RGS5","MEFV","KCNN4","RNMT","TTI1","PLXNB1","TGFB1I1","MTSS1","MAP3K7","RIPK2","WDR62","KLF4","WIPF1","BCL2L11","FOXO3","SPRY2","DCX","SNAI2","PRC1","TCF21","BUB1","BUB3","ACTN4","SGTA","ENSA","SPOP","AHCYL1","AIRE","GMFG","BNIP3L","PRKN","ZEB2","PIP5K1C","KDM1A","TBC1D4","NUPR1","NPHS1","CCNT1","BUB1B","SNAP91","JAK2","CTNND1","PFKFB2","PAGE4","BRD4","TBL1X","NBN","DTNB","DNAJC6","ROCK2","CLASP2","PEX14","ULK1","NR1I2","GMNN","CLDN11","BANF1","DAB1","PRKRA","LRP6","REM1","OFD1","TOM1L1","WDHD1","TRAPPC6A","IDH1","BEST1","RECQL4","URI1","UFL1","SORBS2","SASH1","NFAT5","MFN2","ZWINT","KAT7","EPM2A","SNAPIN","ZBTB7A","MAP3K6","SVIL","AHSA1","KLF8","NFATC1","HERC2","OXSR1","DDX58","AIFM1","SNAI1","MPIG6B","ECD","BCL10","PAK4","CHEK2","APBA3","NSD2","LDHA","ALDH1A1","GLUD1","SOD1","GOT2","ABL1","EGFR","PGK1","FOS","MYC","NRAS","HRAS","KRAS","CRYAB","LMNA","SLC4A1","FTH1","ESR1","RAF1","ANXA1","NR3C1","TK1","MYCN","ERBB2","NTRK1","TP53","HSPB1","ITGB2","HMGN1","JUN","ITGB1","KRT18","LCK","RB1","PGR","EIF4E","NPM1","TH","P4HB","CSF1R","ANXA2","ADRB2","PFN1","EPRS1","HSP90AA1","RET","FH","SP1","RHO","NGFR","GLI1","HSP90AB1","MME","PDHA1","MET","VIM","KRT19","GSTP1","FBP1","HMOX1","PDGFRB","HNRNPA1","TACSTD2","PARP1","H2AZ1","H2AC11","POLR2M","HSPA1A","CALM1","MYBL2","AR","RARA","H1-4","BCL2","PRKAR1A","KIT","CD28","THRB","MCF2","MYL2","HSPA5","MAP2","SLC2A1","BCR","FGFR1","TOP1","TOP2A","VDR","PCNA","CKMT1A","ACTN1","ACE","CDH1","SRC","XRCC6","UNG","CYBA","CFTR","KRT5","TPT1","LCP1","GFAP","SELL","HCLS1","NCF1","PKM","HNRNPL","ETS1","JUP","BRAF","GLUL","ANPEP","MYOD1","EZR","VAV1","NQO1","TCF3","GATA1","TIMP2","H2AX","ITGB4","PDGFRA","KCNA2","H1-2","CTLA4","PRLR","CD36","IL7R","STMN1","IFNAR1","JUNB","GJA1","UBTF","TAL1","PRKACA","CEBPB","CTPS1","DDX5","LGALS3","SPI1","NELFE","RCC1","SDC1","ATF1","ATF6","LIG1","XRCC1","CDH2","MYL12A","PLCG1","ELK1","TNNI3","TNFRSF1A","TRIM21","TFEB","EIF2AK2","SLC9A1","RXRA","ANXA7","CD33","LMNB1","CD247","FLNA","FPR1","CNR1","DRD1","FGFR2","ERBB3","TGM2","CBL","NR4A1","XPA","SFPQ","HRC","MCC","CFL1","EIF4B","GATA2","GATA3","DTYMK","RRM1","CCND1","IL4R","AKAP5","POLR2A","CDK2","APC","GRK2","ACKR3","ITGB7","MSN","DNMT1","PLN","RPA1","APEX1","DCK","PIK3R1","MAPK1","DUSP1","MZF1","RBL1","GRN","ADORA2A","EPHA2","PTPN6","ARID4A","NOS3","PML","GNA11","PEBP1","CD6","CDC27","CCND3","WEE1","MIP","CDC25A","CDC25B","CDC25C","PPIF","AXL","AGTR1","CLIP1","GCH1","SSTR2","CORO1A","MAPK4","HOXA11","RRM2","SDC4","AKT1","SFN","S100A11","L1CAM","ARRB2","CCKBR","CCR7","FOXN2","CIITA","CDH5","H2BC3","TTK","MCM7","SDC2","CTNNA1","CTNNB1","PCGF2","PHB1","NF2","SPRR2B","RORA","DRD3","SCN1A","IRS1","MYH9","ADD1","FUS","DEK","CHKA","FLT4","KDR","MAP2K2","ZNF76","FLT3","TGFBR1","SREBF1","TGFBR2","TAGLN2","SNCA","BRCA1","EIF4A3","CDKN1A","FEN1","IL6ST","CEACAM3","MPL","VHL","STAT3","USP8","ID1","CASR","AQP2","CETN2","GARS1","MAP3K8","STAT1","STAT6","MTOR","CASP2","NCAPD3","WAS","CDKN2A","HTT","MTHFR","MCAM","DCC","ETV4","RAD52","ZAP70","SYK","KIR2DL1","MAPK8","RANGAP1","CRK","NSF","CDKN1B","RPS10","YAP1","UTRN","IQGAP1","RAP1GAP","P2RY1","ME1","SOX2","SOX9","NRIP1","CSNK1A1","IDH2","PIK3CG","PXN","ARRB1","AMPH","CENPA","PCYT1A","STAR","GPR15","CEBPD","MCM2","RBM25","PSEN1","RGS7","PSEN2","TSC2","CDKN1C","MRE11","MMP14","EMD","HTR6","PEX5","VASP","CDK9","RAB7A","SMARCA4","BRCA2","MECP2","IRAK1","CAV2","HSD17B4","AFF1","KPNA2","JAK3","MAP2K6","ARHGDIA","ARHGDIB","STAT2","PLK1","DAPK1","ARFIP1","PTTG1IP","BLM","ATXN1","TERF1","EPHB3","EPHB1","GEM","AQP5","VCP","CASP7","CDKN2D","RAG2","MARS1","ARPP19","HDAC4","BACE1","BCAR1","STX17","CLDN2","FOXL2","PTEN","GABARAPL2","ACTB","SNAP25","CDC42","RAB8A","CXCR4","RAP1B","PSME3","RHOA","RND3","HNRNPK","BTG1","H4C1","RAB1A","RAN","RAP1A","GRB2","RAC1","AP2B1","YWHAZ","DYNLL1","DYNLT1","RACK1","UBE2I","PPP2CA","H3C1","CXADR","SH3BP2","EIF4G2","GTF2I","DLG4","SRPK2","PRKDC","DCD","CBX1","SMAD3","DAB2","XIAP","CDK6","CDK5","CDK16","CLTC","HSF1","NFKB2","HNRNPU","MDM2","E2F1","IL9R","RUNX1","RELB","PFKP","SATB1","POU5F1","TAGLN","GUCY1B1","PRKCE","KIF23","ID3","MAP2K1","AKAP12","MLLT1","MECOM","CAV1","KMT2A","TGFBR3","PPARD","PTS","ERCC6","RELA","EIF4G1","MST1R","YWHAH","SRY","PTPN12","PTK2","PRKCD","CALD1","PTPN11","BTK","MEF2C","RAD51","TJP1","ZFP36L1","BCL2L1","MCL1","POLE","PPARA","SOS1","TNK2","LRP1","FOXM1","DDR1","RBL2","NSUN2","EP300","FOXO1","CETN1","AKAP13","KCNH2","CDC20","GRIN2A","TP53BP1","AIMP1","PTPRJ","EPS8","TRAF2","TIAM1","STK4","FLII","TRIM32","ACACA","LCP2","USP4","TRAF3","KLF10","REST","TARDBP","PAK1","AIMP2","FADD","MAPK7","STK3","CBLB","PSMD2","GRIN2B","MAP3K1","MAD2L1","TRIM28","G3BP1","SKP2","ATM","GRB10","BIK","ITGB3BP","PPP2R5C","CTBP1","PDE3B","PDCL","XRCC4","TCOF1","SF3B2","FKBP5","NFATC2","GAB1","SMAD4","SQSTM1","PIN1","SERINC3","ATR","EIF4EBP1","RIPK1","SNW1","IQGAP2","STIM1","DYRK1A","IL10RA","RIN1","RUNX3","PMAIP1","TNFAIP1","PKP1","KLF5","TOB2","TRIM29","TRIM14","KEAP1","DOC2B","DOCK1","WRN","CTTN","ENDOG","PTK2B","PDE3A","GRB14","GRB7","BECN1","SCN5A","ITPR1","IRF3","ESPL1","MDC1","MELK","SMC1A","NCOA6","MVP","STAT4","CASP8","KIF22","MEF2D","LASP1","STARD3","NOLC1","NR1I3","MAD2L1BP","ABRAXAS2","SUZ12","ACAP1","CDK5R1","AGER","CDK10","PRKD1","PLEC","PTGES3","STK38","RABEP1","RBBP5","ERBB4","SAFB","SEC23A","SEC23B","STIL","TERF2","SLC9A3R2","TRADD","TARBP2","TRIP10","MED1","MAPRE1","ELAVL1","CEBPE","CD226","SMAD2","SMAD1","STK11","STXBP2","EZH2","ZYX","SEPTIN7","CCDC6","NFE2L2","DDB1","CDC37","DPYSL2","C3AR1","MAP3K11","BAK1","AANAT","STX1A","OCLN","SMN1","DBN1","FSCN1","MAPK6","HIF1A","RALGAPA2","PLEKHG6","CCDC88A","TIGIT","CRY2","LARP7","AMOT","LIN52","PDCD4","CRTC2","CEP55","PARP10","SGO1","MIIP","LRRK2","LY6G6F","PDZK1","RNF187","FYB2","FBXO31","RAP1GAP2","CREB3L3","ARHGAP17","CDCA2","FCRL6","LAIR1","SIGIRR","STYK1","TET2","CAVIN1","CDC73","TNFAIP8L2","BORA","RICTOR","ABRAXAS1","MEX3B","CENPU","TUBA1A","GAREM2","SND1","MARK2","ATG9A","MAVS","ARHGAP22","SPRED1","SH3RF1","TBC1D1","METTL3","NOXA1","RIMS1","FHIP2B","SKAP1","STING1","LSR","TICAM1","SIAH1","VRK3","MAP4K3","CCDC50","FUNDC1","MISP","TRIM59","TPH2","CCAR1","SKA3","SIRT2","SEPTIN12","ULK2","ABI1","TAGAP","RPTOR","CCAR2","MTURN","LILRB2","AFAP1L2","CAMKK1","IL22RA1","CGAS","ACOT4","MLKL","HJURP","CCNY","PIK3C3","MCPH1","SHCBP1","DOCK8","ZNRF2","NEDD1","MAFA","COP1","CDC26","MPLKIP","DEPTOR","NEK9","CD200R1","CD300LF","NEK7","ASAP3","CEP192","PARD3","PARD3B","FNIP1","CASTOR1","PPP1R13L","PDCD6IP","BLNK","LEO1","ARAP3","ATRIP","GATAD2B","SSH1","GBF1","TOPBP1","ELMO1","WASF1","BAP1","TSC1","MAML1","NDRG1","AKAP1","ESR2","HDAC2","PROX1","CREBBP","KAT6A","OSTF1","UFD1","UPF1","DAZL","FGF14","BAD","KHSRP","ARHGEF2","BRF1","USP13","SECISBP2L","FBXW7","CNKSR1","OSBP2","L3MBTL2","FERMT2","AKT1S1","SH3KBP1","SPSB1","OTULIN","SGK3","OPTN","KCTD12","PABIR1","SIRT1","DAZAP1","MVB12A","NRBF2","TRIM11","EDC3","CDCA5","C16orf74","ITCH","VCPIP1","PBK","EHMT2","EGLN2","SNX27","PRICKLE1","MUS81","NLRP3","RCHY1","NEDD4L","SLITRK1","ATAD5","CIC","CAMKK2","DCLRE1C","CDK5RAP2","PPP1R16B","UHRF1","NIBAN2","RMDN3","PSMD1","PARK7","PHB2","RAD9A","PKMYT1","KIF2C","MAP3K5","GFI1","DOK1","RBBP8","MAP3K3","APBA2","NKX3-1","EPAS1","ARID3A","PKP2","SH3GL1","SH3GL2","VGLL1","DPYSL5","NABP2","SULT4A1","CORO1B","LZTS2","LARP6","C2orf88","WRAP53","CCDC106","RBM4","CDCA7","BRIP1","RAB11FIP5","BBC3","MAP1LC3C","FANCD2","PACSIN1","ACE2","NIFK","IFIH1","PPP1R12C","PRKD2","NIBAN1","BCL11B","MAP1LC3B","WWTR1","MFF","MAF1","KLC2","RACGAP1","SMG9","RBM38","ISCU","MED28","CDT1","CARD9","HIPK2","CDC42EP4","KDM4C","DNAJC5","CUEDC2","MAP1LC3A","WNK1","GOLPH3","DEF6","CDCP1","RETREG1","GAREM1","PEAK1","PLEKHG2","KAT8","MOB1A","NHEJ1","NANOG","SMURF2","CLSPN","PIDD1","TRPV4","RC3H2","EML4","CENPJ","METTL14","LRRC4C","BRMS1","SH2D2A","GCM1","DMAP1","FZD3","NOX4","CD93","CYLD","INCENP","KIF13B","PAK6","DIABLO","SIRT7","PICK1","DISC1","ARHGAP35","RGS18","TOPORS","SAMSN1","TDP1","PARVA","PRMT7","PAG1","BABAM1","IRAK4","NDE1","AATF","SPHK1","DACT1","RRN3","CLIC5","WWOX","DTL","NOP53","CD274","KLRF1","PDP1","ADAM22","SH3BP4","CCDC88C","ABI3","EIF2AK4","UVRAG","ATXN10","TRPC4","HDAC6","ZMYM2","ZNF282","MALT1","DAXX","STAP2","POLL","SEC63","SWAP70","KLHL3","TBK1","GTF2IRD1","BAIAP2L1","ATP5IF1","ERRFI1","LEF1","DBNL","DDX41","GGA1","USP21","PITPNC1","APPL1","FBXO4","AGO2","ASAP1","HSF4","CBLC","FZR1","ALK","DDX19B","SUFU","PACSIN2","FAF1","ABCG2","TIMELESS","CEP131","TRIM33","PHF8","EXOC7","MAPRE3","SHOC2","PA2G4","EXO1","BAIAP2","GAB2","MAPK8IP1","HDAC5","CAMK2A","RUVBL2","ASF1A","NINL","AMOTL2","SIK3","USP20","PTPN22","MAP3K2","LEMD3","GIT1","ZNF281","UBE2J1","CBY1","SIT1","PKP3","KIF3A","KDM3A","DAAM1","USP15","RAPGEF2","ATG4B","TELO2","RIPK3","RBM7","CTDP1","CLDN16","CERT1","USP16","INSIG2","SNX8","SNX5","LRRFIP2","F11R","MAD1L1","SNCAIP","IKBKG","NCOA3","MORC2"];
    var uniprots = ["A9UF07","C9JLW8","O00161","O00170","O00213","O00257","O00308","O00399","O00418","O00459","O00499","O00541","O00560","O00571","O00629","O14493","O14543","O14559","O14641","O14654","O14727","O14745","O14746","O14757","O14796","O14974","O15105","O15117","O15151","O15162","O15164","O15217","O15259","O15287","O15350","O15379","O15392","O15503","O15516","O15524","O15530","O15539","O15553","O15554","O43148","O43156","O43157","O43294","O43312","O43318","O43353","O43379","O43474","O43516","O43521","O43524","O43597","O43602","O43623","O43663","O43680","O43683","O43684","O43707","O43765","O43768","O43791","O43865","O43918","O60234","O60238","O60260","O60315","O60331","O60341","O60343","O60356","O60500","O60563","O60566","O60641","O60674","O60716","O60825","O60829","O60885","O60907","O60934","O60941","O75061","O75116","O75122","O75381","O75385","O75469","O75496","O75508","O75531","O75553","O75569","O75581","O75628","O75665","O75674","O75717","O75865","O75874","O76090","O94761","O94763","O94874","O94875","O94885","O94916","O95140","O95229","O95251","O95278","O95295","O95365","O95382","O95425","O95433","O95600","O95644","O95714","O95747","O95786","O95831","O95863","O95866","O95905","O95999","O96013","O96017","O96018","O96028","P00338","P00352","P00367","P00441","P00505","P00519","P00533","P00558","P01100","P01106","P01111","P01112","P01116","P02511","P02545","P02730","P02794","P03372","P04049","P04083","P04150","P04183","P04198","P04626","P04629","P04637","P04792","P05107","P05114","P05412","P05556","P05783","P06239","P06400","P06401","P06730","P06748","P07101","P07237","P07333","P07355","P07550","P07737","P07814","P07900","P07949","P07954","P08047","P08100","P08138","P08151","P08238","P08473","P08559","P08581","P08670","P08727","P09211","P09467","P09601","P09619","P09651","P09758","P09874","P0C0S5","P0C0S8","P0CAP2","P0DMV8","P0DP23","P10244","P10275","P10276","P10412","P10415","P10644","P10721","P10747","P10828","P10911","P10916","P11021","P11137","P11166","P11274","P11362","P11387","P11388","P11473","P12004","P12532","P12814","P12821","P12830","P12931","P12956","P13051","P13498","P13569","P13647","P13693","P13796","P14136","P14151","P14317","P14598","P14618","P14866","P14921","P14923","P15056","P15104","P15144","P15172","P15311","P15498","P15559","P15923","P15976","P16035","P16104","P16144","P16234","P16389","P16403","P16410","P16471","P16671","P16871","P16949","P17181","P17275","P17302","P17480","P17542","P17612","P17676","P17812","P17844","P17931","P17947","P18615","P18754","P18827","P18846","P18850","P18858","P18887","P19022","P19105","P19174","P19419","P19429","P19438","P19474","P19484","P19525","P19634","P19793","P20073","P20138","P20700","P20963","P21333","P21462","P21554","P21728","P21802","P21860","P21980","P22681","P22736","P23025","P23246","P23327","P23508","P23528","P23588","P23769","P23771","P23919","P23921","P24385","P24394","P24588","P24928","P24941","P25054","P25098","P25106","P26010","P26038","P26358","P26678","P27694","P27695","P27707","P27986","P28482","P28562","P28698","P28749","P28799","P29274","P29317","P29350","P29374","P29474","P29590","P29992","P30086","P30203","P30260","P30281","P30291","P30301","P30304","P30305","P30307","P30405","P30530","P30556","P30622","P30793","P30874","P31146","P31152","P31270","P31350","P31431","P31749","P31947","P31949","P32004","P32121","P32239","P32248","P32314","P33076","P33151","P33778","P33981","P33993","P34741","P35221","P35222","P35227","P35232","P35240","P35325","P35398","P35462","P35498","P35568","P35579","P35611","P35637","P35659","P35790","P35916","P35968","P36507","P36508","P36888","P36897","P36956","P37173","P37802","P37840","P38398","P38919","P38936","P39748","P40189","P40198","P40238","P40337","P40763","P40818","P41134","P41180","P41181","P41208","P41250","P41279","P42224","P42226","P42345","P42575","P42695","P42768","P42771","P42858","P42898","P43121","P43146","P43268","P43351","P43403","P43405","P43626","P45983","P46060","P46108","P46459","P46527","P46783","P46937","P46939","P46940","P47736","P47900","P48163","P48431","P48436","P48552","P48729","P48735","P48736","P49023","P49407","P49418","P49450","P49585","P49675","P49685","P49716","P49736","P49756","P49768","P49802","P49810","P49815","P49918","P49959","P50281","P50402","P50406","P50542","P50552","P50750","P51149","P51532","P51587","P51608","P51617","P51636","P51659","P51825","P52292","P52333","P52564","P52565","P52566","P52630","P53350","P53355","P53367","P53801","P54132","P54253","P54274","P54753","P54762","P55040","P55064","P55072","P55210","P55273","P55895","P56192","P56211","P56524","P56817","P56945","P56962","P57739","P58012","P60484","P60520","P60709","P60880","P60953","P61006","P61073","P61224","P61289","P61586","P61587","P61978","P62324","P62805","P62820","P62826","P62834","P62993","P63000","P63010","P63104","P63167","P63172","P63244","P63279","P67775","P68431","P78310","P78314","P78344","P78347","P78352","P78362","P78527","P81605","P83916","P84022","P98082","P98170","Q00534","Q00535","Q00536","Q00610","Q00613","Q00653","Q00839","Q00987","Q01094","Q01113","Q01196","Q01201","Q01813","Q01826","Q01860","Q01995","Q02153","Q02156","Q02241","Q02535","Q02750","Q02952","Q03111","Q03112","Q03135","Q03164","Q03167","Q03181","Q03393","Q03468","Q04206","Q04637","Q04912","Q04917","Q05066","Q05209","Q05397","Q05655","Q05682","Q06124","Q06187","Q06413","Q06609","Q07157","Q07352","Q07817","Q07820","Q07864","Q07869","Q07889","Q07912","Q07954","Q08050","Q08345","Q08999","Q08J23","Q09472","Q12778","Q12798","Q12802","Q12809","Q12834","Q12879","Q12888","Q12904","Q12913","Q12929","Q12933","Q13009","Q13043","Q13045","Q13049","Q13085","Q13094","Q13107","Q13114","Q13118","Q13127","Q13148","Q13153","Q13155","Q13158","Q13164","Q13188","Q13191","Q13200","Q13224","Q13233","Q13257","Q13263","Q13283","Q13309","Q13315","Q13322","Q13323","Q13352","Q13362","Q13363","Q13370","Q13371","Q13426","Q13428","Q13435","Q13451","Q13469","Q13480","Q13485","Q13501","Q13526","Q13530","Q13535","Q13541","Q13546","Q13573","Q13576","Q13586","Q13627","Q13651","Q13671","Q13761","Q13794","Q13829","Q13835","Q13887","Q14106","Q14134","Q14142","Q14145","Q14184","Q14185","Q14191","Q14247","Q14249","Q14289","Q14432","Q14449","Q14451","Q14457","Q14524","Q14643","Q14653","Q14674","Q14676","Q14680","Q14683","Q14686","Q14764","Q14765","Q14790","Q14807","Q14814","Q14847","Q14849","Q14978","Q14994","Q15013","Q15018","Q15022","Q15027","Q15078","Q15109","Q15131","Q15139","Q15149","Q15185","Q15208","Q15276","Q15291","Q15303","Q15424","Q15436","Q15437","Q15468","Q15554","Q15599","Q15628","Q15633","Q15642","Q15648","Q15691","Q15717","Q15744","Q15762","Q15796","Q15797","Q15831","Q15833","Q15910","Q15942","Q16181","Q16204","Q16236","Q16531","Q16543","Q16555","Q16581","Q16584","Q16611","Q16613","Q16623","Q16625","Q16637","Q16643","Q16658","Q16659","Q16665","Q2PPJ7","Q3KR16","Q3V6T2","Q495A1","Q49AN0","Q4G0J3","Q4VCS5","Q52LA3","Q53EL6","Q53ET0","Q53EZ4","Q53GL7","Q5FBB7","Q5JXC2","Q5S007","Q5SQ64","Q5T2W1","Q5TA31","Q5VWT5","Q5XUX0","Q684P5","Q68CJ9","Q68EM7","Q69YH5","Q6DN72","Q6GTX8","Q6IA17","Q6J9G0","Q6N021","Q6NZI2","Q6P1J9","Q6P589","Q6PGQ7","Q6R327","Q6UWZ7","Q6ZN04","Q71F23","Q71U36","Q75VX8","Q7KZF4","Q7KZI7","Q7Z3C6","Q7Z434","Q7Z5H3","Q7Z699","Q7Z6J0","Q86TI0","Q86U44","Q86UR1","Q86UR5","Q86V87","Q86WV1","Q86WV6","Q86X29","Q8IUC6","Q8IUQ4","Q8IV63","Q8IVH8","Q8IVM0","Q8IVP5","Q8IVT2","Q8IWR1","Q8IWU9","Q8IX12","Q8IX90","Q8IXJ6","Q8IYM1","Q8IYT8","Q8IZP0","Q8N103","Q8N122","Q8N163","Q8N3F0","Q8N423","Q8N4X5","Q8N5S9","Q8N6P7","Q8N884","Q8N9L9","Q8NB16","Q8NCD3","Q8ND76","Q8NEB9","Q8NEM0","Q8NEM2","Q8NF50","Q8NHG8","Q8NHV4","Q8NHW3","Q8NHY2","Q8NHZ8","Q8TAP9","Q8TB45","Q8TD19","Q8TD46","Q8TDQ1","Q8TDX7","Q8TDY4","Q8TEP8","Q8TEW0","Q8TEW8","Q8TF40","Q8WTX7","Q8WUF5","Q8WUM4","Q8WV28","Q8WVC0","Q8WWN8","Q8WXE1","Q8WXI9","Q8WYL5","Q92538","Q92547","Q92556","Q92558","Q92560","Q92574","Q92585","Q92597","Q92667","Q92731","Q92769","Q92786","Q92793","Q92794","Q92882","Q92890","Q92900","Q92904","Q92915","Q92934","Q92945","Q92974","Q92994","Q92995","Q93073","Q969H0","Q969H4","Q969R2","Q969R5","Q96AC1","Q96B36","Q96B97","Q96BD6","Q96BN8","Q96BR1","Q96CV9","Q96CX2","Q96E09","Q96EB6","Q96EP5","Q96EY5","Q96F24","Q96F44","Q96F86","Q96FF9","Q96GX8","Q96J02","Q96JH7","Q96KB5","Q96KQ7","Q96KS0","Q96L92","Q96MT3","Q96NY9","Q96P20","Q96PM5","Q96PU5","Q96PX8","Q96QE3","Q96RK0","Q96RR4","Q96SD1","Q96SN8","Q96T49","Q96T88","Q96TA1","Q96TC7","Q99460","Q99497","Q99623","Q99638","Q99640","Q99661","Q99683","Q99684","Q99704","Q99708","Q99759","Q99767","Q99801","Q99814","Q99856","Q99959","Q99961","Q99962","Q99990","Q9BPU6","Q9BQ15","Q9BR01","Q9BR76","Q9BRK4","Q9BRS8","Q9BSF0","Q9BUR4","Q9BWC9","Q9BWF3","Q9BWT1","Q9BX63","Q9BXF6","Q9BXH1","Q9BXW4","Q9BXW9","Q9BY11","Q9BYF1","Q9BYG3","Q9BYX4","Q9BZL4","Q9BZL6","Q9BZQ8","Q9C0K0","Q9GZQ8","Q9GZV5","Q9GZY8","Q9H063","Q9H0B6","Q9H0H5","Q9H0W8","Q9H0Z9","Q9H1K1","Q9H204","Q9H211","Q9H257","Q9H2X6","Q9H3Q1","Q9H3R0","Q9H3Z4","Q9H467","Q9H492","Q9H4A3","Q9H4A6","Q9H4E7","Q9H5V8","Q9H6L5","Q9H706","Q9H792","Q9H7P9","Q9H7Z6","Q9H8S9","Q9H9Q4","Q9H9S0","Q9HAU4","Q9HAW4","Q9HB75","Q9HBA0","Q9HBD1","Q9HC35","Q9HC77","Q9HCE5","Q9HCJ2","Q9HCU9","Q9NP31","Q9NP62","Q9NPF5","Q9NPG1","Q9NPH5","Q9NPY3","Q9NQC7","Q9NQS7","Q9NQT8","Q9NQU5","Q9NR28","Q9NRC8","Q9NRD5","Q9NRI5","Q9NRY4","Q9NS28","Q9NS56","Q9NSI8","Q9NUW8","Q9NVD7","Q9NVM4","Q9NWQ8","Q9NWV8","Q9NWZ3","Q9NXR1","Q9NY61","Q9NYA1","Q9NYF0","Q9NYV6","Q9NZA1","Q9NZC7","Q9NZJ0","Q9NZM5","Q9NZQ7","Q9NZS2","Q9P0J1","Q9P0K1","Q9P0V3","Q9P219","Q9P2A4","Q9P2K8","Q9P2Y5","Q9UBB4","Q9UBN4","Q9UBN7","Q9UBW7","Q9UDV7","Q9UDY8","Q9UER7","Q9UGK3","Q9UGP5","Q9UGP8","Q9UH65","Q9UH77","Q9UHD2","Q9UHL9","Q9UHR4","Q9UII2","Q9UJM3","Q9UJU2","Q9UJU6","Q9UJV9","Q9UJY5","Q9UK80","Q9UKF7","Q9UKG1","Q9UKT5","Q9UKV8","Q9ULH1","Q9ULV5","Q9ULV8","Q9UM11","Q9UM73","Q9UMR2","Q9UMX1","Q9UNF0","Q9UNN5","Q9UNQ0","Q9UNS1","Q9UPN4","Q9UPN9","Q9UPP1","Q9UPT5","Q9UPY8","Q9UQ13","Q9UQ80","Q9UQ84","Q9UQB8","Q9UQC2","Q9UQF2","Q9UQL6","Q9UQM7","Q9Y230","Q9Y294","Q9Y2I6","Q9Y2J4","Q9Y2K2","Q9Y2K6","Q9Y2R2","Q9Y2U5","Q9Y2U8","Q9Y2X7","Q9Y2X9","Q9Y385","Q9Y3M2","Q9Y3P8","Q9Y446","Q9Y496","Q9Y4C1","Q9Y4D1","Q9Y4E8","Q9Y4G8","Q9Y4P1","Q9Y4R8","Q9Y572","Q9Y580","Q9Y5B0","Q9Y5I7","Q9Y5P4","Q9Y5T5","Q9Y5U4","Q9Y5X2","Q9Y5X3","Q9Y608","Q9Y624","Q9Y6D9","Q9Y6H5","Q9Y6K9","Q9Y6Q9","Q9Y6X9"];
    let $gene = document.getElementById("gene")
    let $uniprot = document.getElementById("uniprot")
	if($gene)autocomplete($gene, genes);
	if($uniprot)autocomplete($uniprot, uniprots);
} );
