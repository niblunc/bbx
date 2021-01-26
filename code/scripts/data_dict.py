import os, glob
import pandas as pd
from IPython.display import display


"""
# BBX Calculations
# by Nichollette Acosta

## Program takes in raw behavioral files (.tsv)

"""

class DataDict():

    def __init__(self, data_path):
        self.data_path=data_path

    def load_data(self):
        """
        """
        data_path=self.data_path
        #print('[INFO] data path %s'%self.data_path)
        #behav_df = pd.read_csv(os.path.join(data_path, "bbx_msBxScn_datadict_12_30_20.xlsx"))
        df = pd.read_excel(os.path.join(data_path,  "bbx_msBxScn_datadict_12_30_20.xlsx"), sheet_name='scoring')
        #display(df)
        #print(df.columns.values)
        
    
    """
    # FFQ : Food Frequency Questionnaire
    """
    def ffq_calculation():
        
        # Set Variables
        ffq_dict={}
        s1_behav_copy=s1_behav    
        
        # loop through the ffq## values(columns)
        for col_val in s1_behav.filter(like="ffq", axis=1).columns.values:
            
            # extract ffq numerical id
            id_val=col_val.split("_")[2]
            # add id to dictionary
            
            # create string with numerical id to search in nutrient document
            ffq_id="ffq%s"%id_val
            #print("\n[INFO] getting %s calculations"%(ffq_id))
    
            # -- Get nutrient ffq averages --
            # get kcal_ffq##
            kcal_ffq=float(nutrient_info.loc[ffq_id, 'kcal/100g'])
    
            # get fat_ffq##
            fat_ffq=float(nutrient_info.loc[ffq_id, 'fat(g)/100g'])
    
            # get sug_ffq
            sug_ffq=float(nutrient_info.loc[ffq_id, 'sugars/100g'])
    
            # grams/med portion 
            grams_portion=float(nutrient_info.loc[ffq_id, 'grams/med portion '])
    
            # prepare the column -- translte into numeric to run calculations
            s1_behav_copy[col_val]=pd.to_numeric(s1_behav_copy[col_val], errors='coerce')
            z=np.asarray(s1_behav_copy[col_val])
            #print("\n[INFO] original data: \n", wBx_ffq[:10])
    
            for bbx_id in s1_behav.index.values:
                if bbx_id not in ffq_dict:
                    ffq_dict[bbx_id]={}
       
                """
                # Apply reverse scoring to the ffq_## value
                """
                s1_behav_copy[col_val] = s1_behav_copy[col_val].replace([1,2,3,4,5,6],[0,2,5,8,11.5, 14])
    
                # get row
                ffq_val=s1_behav_copy.loc[bbx_id,col_val]
                
                """
                # Calculations
                """
                # -- Calculations --
    
                # --FFQ--
    
                # -- ffq##_kcal -- 
                w1ffq_kcal=ffq_val*kcal_ffq*(grams_portion/100)
                #print("\n[INFO] %s * %s"%(col_val, kcal_ffq))
                #print("[INFO] kcal data: \n", w1ffq_kcal[:10]
    
                # -- ffq##_gfat -- 
                w1ffq_gfat=ffq_val*fat_ffq
                #print("\n[INFO] %s * %s"%(col_val, fat_ffq))
                #print("[INFO] gfat data: \n", w1ffq_gfat)
    
                # -- ffq##_fatkcal -- 
                w1ffq_fatkcal=w1ffq_gfat*9
                #print("[INFO] fatkcal data: ", w1ffq_fatkcal)
    
                # -- ffq##_gsug -- 
                w1ffq_gsug=ffq_val*sug_ffq
                #print("\n[INFO] %s * %s"%(col_val, sug_ffq))
                #print("[INFO] gsug data: \n", w1ffq_gsug)
    
                # -- ffq##_sugkcal --
                w1ffq_sugkcal = w1ffq_gsug*4
                #print("[INFO] sugkcal data: ", w1ffq_sugkcal)
    
                # -- Fill Dictionary --
                ffq_dict[bbx_id]['w1Bx_ffq_%s_kcal'%id_val]=w1ffq_kcal
                ffq_dict[bbx_id]['w1Bx_ffq_%s_gfat'%id_val]=w1ffq_gfat
                ffq_dict[bbx_id]['w1Bx_ffq_%s_fatkcal'%id_val]=w1ffq_fatkcal
                ffq_dict[bbx_id]['w1Bx_ffq_%s_gsug'%id_val]=w1ffq_gsug 
                ffq_dict[bbx_id]['w1Bx_ffq_%s_sugkcal'%id_val]=w1ffq_sugkcal 
    
        # Create dataframe from dicionary
        ffq_df= pd.DataFrame(ffq_dict).T  
        # Filter dataframe into specific sets for calculations
        kcal_df=ffq_df.filter(like="kcal", axis=1)
        fatkcal_df=ffq_df.filter(like="fatkcal", axis=1)
        gsug_df=ffq_df.filter(like="gsug", axis=1)
        sugkcal_df=ffq_df.filter(like="sugkcal", axis=1)
    
        for bbx_id in s1_behav.index.values:
            """
            # Set Rows
            """
            kcal_row=kcal_df.loc[bbx_id,:]
            fatkcal_row=fatkcal_df.loc[bbx_id,:]  
            sugkcal_row=sugkcal_df.loc[bbx_id, :]
    
            """
            # Calculations 
            """
            # --avgkcal --
            avgkcal=sum(kcal_row)/14
    
            # -- avgfatkcal -
            avgfatkcal = sum(fatkcal_row)/14
    
            # -- pctfat --
            pctfat=(sum(fatkcal_row)/sum(kcal_row))*100
            pctfat_d = (avgfatkcal/avgkcal)*100
    
            # -- avgsugkcal --
            avgsugkcal=sum(sugkcal_row)/14
    
            # -- pctsug --
            pctsug=(sum(sugkcal_row)/sum(kcal_row))*100
            pctsug_d=(avgsugkcal/avgkcal)*100
    
            """
            # Add to dictionary
            """
            # -- Fill Dictionary --
            ffq_dict[bbx_id]['w1ffq_avgkcal']=avgkcal
            ffq_dict[bbx_id]['w1ffq_avgfatkcal']=avgfatkcal
            ffq_dict[bbx_id]['w1ffq_avgsugkcal']=avgsugkcal
            ffq_dict[bbx_id]['w1ffq_pctfat']=pctfat
            ffq_dict[bbx_id]['w1ffq_pctfat_d']=pctfat_d
            ffq_dict[bbx_id]['w1ffq_pctsug']=pctsug
            ffq_dict[bbx_id]['w1ffq_pctsug_d']=pctsug_d
            
        """
        # Generate Output
        """
        
        # make dataframe 
        ffq_df_final= pd.DataFrame(ffq_dict).T  
        #display(ffq_df_final.head())
        
        reverse_data=s1_behav_copy.filter(like="ffq", axis=1)
        ffq_reverse_data=pd.DataFrame(reverse_data)
        #display(ffq_reverse_data.head())
        
        # wrote tp csv
        #path="C:\Users\19802\Documents\nibl\bbx_test_outputs"
        ffq_df_final.to_csv(os.path.join(output_path,"w1Bx_ffq_calculations.csv"))
        ffq_reverse_data.to_csv(os.path.join(output_path,"w1Bx_ffq_reverse_scores.csv"))
        
        ffq_summary_df=ffq_df_final[["w1ffq_avgkcal", "w1ffq_avgfatkcal",
                               "w1ffq_pctfat", "w1ffq_pctfat_d", "w1ffq_avgsugkcal", "w1ffq_pctsug", "w1ffq_pctsug_d" ]]
        
        ffq_summary_df.to_csv(os.path.join(output_path, 'w1Bx_ffq_summary_variables.csv'))
        
        print('\n[INFO] completed FFQ calculations.\n')
        return ffq_df_final, ffq_reverse_data;
    
        # ---
        
        
    
def test():
    """
    test() method 
    """
    data_folder='C:\\Users\\19802\\Documents\\nibl'
    s1_behavioral=(os.path.join(data_path, "bbx_w1_msBxScn_01_06_21.tsv"))
    test= DataDict(data_folder)
    test.load_data()

"""
# inputs expected
# data folder
# datafile mainly

"""

"""
# Methods for Calculations 
"""
def ffq_calculations():
    
    """
    # Set Variables
    """
    ffq_dict={}
    s1_behav_copy=s1_behav    
    
    # loop through the ffq## values(columns)
    for col_val in s1_behav.filter(like="ffq", axis=1).columns.values:
        #(col_val)

        """
        # Set Variables
        """    
        # extract ffq numerical id
        id_val=col_val.split("_")[2]
        # add id to dictionary


        # create string with numerical id to search in nutrient document
        ffq_id="ffq%s"%id_val
        #print("\n[INFO] getting %s calculations"%(ffq_id))

        # -- Get nutrient ffq averages --
        # get kcal_ffq##
        kcal_ffq=float(nutrient_info.loc[ffq_id, 'kcal/100g'])

        # get fat_ffq##
        fat_ffq=float(nutrient_info.loc[ffq_id, 'fat(g)/100g'])

        # get sug_ffq
        sug_ffq=float(nutrient_info.loc[ffq_id, 'sugars/100g'])

        # grams/med portion 
        grams_portion=float(nutrient_info.loc[ffq_id, 'grams/med portion '])

        # prepare the column -- translte into numeric to run calculations
        s1_behav_copy[col_val]=pd.to_numeric(s1_behav_copy[col_val], errors='coerce')
        z=np.asarray(s1_behav_copy[col_val])
        #print("\n[INFO] original data: \n", wBx_ffq[:10])

        for bbx_id in s1_behav.index.values:
            if bbx_id not in ffq_dict:
                ffq_dict[bbx_id]={}

   
            """
            # Apply reverse scoring to the ffq_## value
            """
            s1_behav_copy[col_val] = s1_behav_copy[col_val].replace([1,2,3,4,5,6],[0,2,5,8,11.5, 14])

            # get row
            ffq_val=s1_behav_copy.loc[bbx_id,col_val]
            
            """
            # Calculations
            """
            # -- Calculations --

            # --FFQ--

            # -- ffq##_kcal -- 
            w1ffq_kcal=ffq_val*kcal_ffq*(grams_portion/100)
            #print("\n[INFO] %s * %s"%(col_val, kcal_ffq))
            #print("[INFO] kcal data: \n", w1ffq_kcal[:10]

            # -- ffq##_gfat -- 
            w1ffq_gfat=ffq_val*fat_ffq
            #print("\n[INFO] %s * %s"%(col_val, fat_ffq))
            #print("[INFO] gfat data: \n", w1ffq_gfat)

            # -- ffq##_fatkcal -- 
            w1ffq_fatkcal=w1ffq_gfat*9
            #print("[INFO] fatkcal data: ", w1ffq_fatkcal)

            # -- ffq##_gsug -- 
            w1ffq_gsug=ffq_val*sug_ffq
            #print("\n[INFO] %s * %s"%(col_val, sug_ffq))
            #print("[INFO] gsug data: \n", w1ffq_gsug)

            # -- ffq##_sugkcal --
            w1ffq_sugkcal = w1ffq_gsug*4
            #print("[INFO] sugkcal data: ", w1ffq_sugkcal)

            # -- Fill Dictionary --
            ffq_dict[bbx_id]['w1Bx_ffq_%s_kcal'%id_val]=w1ffq_kcal
            ffq_dict[bbx_id]['w1Bx_ffq_%s_gfat'%id_val]=w1ffq_gfat
            ffq_dict[bbx_id]['w1Bx_ffq_%s_fatkcal'%id_val]=w1ffq_fatkcal
            ffq_dict[bbx_id]['w1Bx_ffq_%s_gsug'%id_val]=w1ffq_gsug 
            ffq_dict[bbx_id]['w1Bx_ffq_%s_sugkcal'%id_val]=w1ffq_sugkcal 


    # Create dataframe from dicionary
    ffq_df= pd.DataFrame(ffq_dict).T  
    # Filter dataframe into specific sets for calculations
    kcal_df=ffq_df.filter(like="kcal", axis=1)
    fatkcal_df=ffq_df.filter(like="fatkcal", axis=1)
    gsug_df=ffq_df.filter(like="gsug", axis=1)
    sugkcal_df=ffq_df.filter(like="sugkcal", axis=1)

    for bbx_id in s1_behav.index.values:
        """
        # Set Rows
        """
        kcal_row=kcal_df.loc[bbx_id,:]
        fatkcal_row=fatkcal_df.loc[bbx_id,:]  
        sugkcal_row=sugkcal_df.loc[bbx_id, :]

        """
        # Calculations 
        """
        # --avgkcal --
        avgkcal=sum(kcal_row)/14

        # -- avgfatkcal -
        avgfatkcal = sum(fatkcal_row)/14

        # -- pctfat --
        pctfat=(sum(fatkcal_row)/sum(kcal_row))*100
        pctfat_d = (avgfatkcal/avgkcal)*100

        # -- avgsugkcal --
        avgsugkcal=sum(sugkcal_row)/14

        # -- pctsug --
        pctsug=(sum(sugkcal_row)/sum(kcal_row))*100
        pctsug_d=(avgsugkcal/avgkcal)*100



        """
        # Add to dictionary
        """
        # -- Fill Dictionary --
        ffq_dict[bbx_id]['w1ffq_avgkcal']=avgkcal
        ffq_dict[bbx_id]['w1ffq_avgfatkcal']=avgfatkcal
        ffq_dict[bbx_id]['w1ffq_avgsugkcal']=avgsugkcal
        ffq_dict[bbx_id]['w1ffq_pctfat']=pctfat
        ffq_dict[bbx_id]['w1ffq_pctfat_d']=pctfat_d
        ffq_dict[bbx_id]['w1ffq_pctsug']=pctsug
        ffq_dict[bbx_id]['w1ffq_pctsug_d']=pctsug_d
        
    """
    # Generate Output
    """
    
    # make dataframe 
    ffq_df_final= pd.DataFrame(ffq_dict).T  
    display(ffq_df_final.head())
    
    # wrote tp csv
    #path="C:\Users\19802\Documents\nibl\bbx_test_outputs"
    ffq_df_final.to_csv(os.path.join(output_path,"w1Bx_ffq_calculations.csv"))
    ffq_summary_df=ffq_df_final[["w1ffq_avgkcal", "w1ffq_avgfatkcal",
                           "w1ffq_pctfat", "w1ffq_pctfat_d", "w1ffq_avgsugkcal", "w1ffq_pctsug", "w1ffq_pctsug_d" ]]
    ffq_summary_df.to_csv(os.path.join(output_path, 'w1Bx_ffq_summary_variables.csv'))
    print('\n[INFO] completed FFQ calculations.\n')
    return ffq_df_final;
                        
"""
# BIS Calculation
"""
                        
def bis_calculation():
    # set starting variables
    bis_dict={}
    error_ids=[]
    s1_behav_copy=s1_behav        
    
    """
    # Reverse Scoring 
    """
    
    s1_behav_copy["w1Bx_bis_6"] = s1_behav_copy["w1Bx_bis_6"].replace([4,3,2,1], [1,2,3,4])    
    s1_behav_copy["w1Bx_bis_7"] = s1_behav_copy["w1Bx_bis_7"].replace([4,3,2,1], [1,2,3,4])
    s1_behav_copy["w1Bx_bis_8"] = s1_behav_copy["w1Bx_bis_8"].replace([4,3,2,1], [1,2,3,4])
    s1_behav_copy["w1Bx_bis_9"] = s1_behav_copy["w1Bx_bis_9"].replace([4,3,2,1], [1,2,3,4])
    s1_behav_copy["w1Bx_bis_10"] = s1_behav_copy["w1Bx_bis_10"].replace([4,3,2,1], [1,2,3,4])
    s1_behav_copy["w1Bx_bis_13"] = s1_behav_copy["w1Bx_bis_13"].replace([4,3,2,1], [1,2,3,4])

    
    for col_val in s1_behav.filter(regex="bis_[0-9]", axis=1).columns.values:
        bis_df=s1_behav_copy.filter(regex="bis_[0-9]", axis=1)
        bis_df=bis_df.apply(pd.to_numeric,  errors='coerce')
        id_val=col_val.split("_")[2]

        """
        # Calculations
        """


        for bbx_id in s1_behav.index.values:
            try:
                # -- bis_tot -- 
                bis_tot=sum(bis_df.loc[bbx_id,:])

                # -- bis_npi --
                bis_npi=sum(bis_df.loc[bbx_id,['w1Bx_bis_6', 'w1Bx_bis_7', 'w1Bx_bis_8', 'w1Bx_bis_9', 'w1Bx_bis_10']])

                # -- bis_mi -- 
                bis_mi=sum(bis_df.loc[bbx_id,['w1Bx_bis_1', 'w1Bx_bis_2', 'w1Bx_bis_3', 'w1Bx_bis_4', 'w1Bx_bis_5']])

                # -- bis_ai --
                bis_ai=sum(bis_df.loc[bbx_id,['w1Bx_bis_11', 'w1Bx_bis_12', 'w1Bx_bis_13', 'w1Bx_bis_14', 'w1Bx_bis_15']])

            except:
                error_ids.append(bbx_id)

            # set dictionary
            if bbx_id not in bis_dict:
                bis_dict[bbx_id]={}

            # add values to dictionary
            bis_dict[bbx_id]["w1bis_tot"]=bis_tot
            bis_dict[bbx_id]["w1bis_npi"]=bis_npi
            bis_dict[bbx_id]["w1bis_mi"]=bis_mi
            bis_dict[bbx_id]["w1bis_ai"]=bis_ai

    if not error_ids:
        pass
    else:
        print("\n[INFO] ERROR with BIS-15 calculation for ids: ",set(error_ids))
    
    # make dataframe 
    
    bis_df_final= pd.DataFrame(bis_dict).T  
    #display(bis_df_final.tail())
    
    bis_df_final.to_csv(os.path.join(output_path, "w1Bx_bis-15_calculations.csv"))
    print('\n[INFO] completed BIS-15 calculations.\n')
    
    
    return bis_df_final;


def fci_calculation():
    # set starting variables
    fci_dict={}
    error_ids=[]
    s1_behav_copy=s1_behav

    df=s1_behav_copy.filter(regex="fci", axis=1)
    df=df.apply(pd.to_numeric,  errors='coerce')
    #id_val=col_val.split("_")[2]
    fciCrv_df=df.filter(regex="fciCrv", axis=1)
    fciLik_df=df.filter(regex="fciLik", axis=1)
    
    
    """
    # Calculations
    """

    for bbx_id in s1_behav.index.values:
        try:
            # -- fci_crave --
            #fciCrv_sum=sum(fciCrv_df.loc[bbx_id, :])
            #fciCrv_ct=len(fciCrv_df.columns.values)
            #fci_crave=fciCrv_sum/fciCrv_ct
            fci_crave=fciCrv_df.loc[bbx_id, :].mean()

            # -- fci_chf --
            fci_chf=fciCrv_df.loc[bbx_id,['w1Bx_fciCrv_3' , 'w1Bx_fciCrv_6' , 'w1Bx_fciCrv_4' , 'w1Bx_fciCrv_15' ,
                                          'w1Bx_fciCrv_26' , 'w1Bx_fciCrv_19' , 'w1Bx_fciCrv_10' , 'w1Bx_fciCrv_27']].mean()

            # -- fci_cs -- 
            fci_cs=fciCrv_df.loc[bbx_id,['w1Bx_fciCrv_25' , 'w1Bx_fciCrv_16' , 'w1Bx_fciCrv_24' , 'w1Bx_fciCrv_17' , 'w1Bx_fciCrv_23' , 'w1Bx_fciCrv_1', 'w1Bx_fciCrv_8' , 'w1Bx_fciCrv_13']].mean()

            # -- fci_cs -- 
            fci_cc=fciCrv_df.loc[bbx_id,['w1Bx_fciCrv_21' , 'w1Bx_fciCrv_18' , 'w1Bx_fciCrv_12' , 'w1Bx_fciCrv_5' , 'w1Bx_fciCrv_9' , 'w1Bx_fciCrv_28' , 'w1Bx_fciCrv_14' , 'w1Bx_fciCrv_22']].mean()

            # -- fci_cs -- 
            fci_cff=fciCrv_df.loc[bbx_id,['w1Bx_fciCrv_11' , 'w1Bx_fciCrv_7' , 'w1Bx_fciCrv_20' , 'w1Bx_fciCrv_2']].mean()


            fci_like=fciLik_df.loc[bbx_id, :].mean()

            fci_lhf=fciLik_df.loc[bbx_id,['w1Bx_fciLik_3' , 'w1Bx_fciLik_6' , 'w1Bx_fciLik_4' , 'w1Bx_fciLik_15' , 'w1Bx_fciLik_26' , 'w1Bx_fciLik_19' , 'w1Bx_fciLik_10' , 'w1Bx_fciLik_27']].mean()

            fci_ls=fciLik_df.loc[bbx_id,['w1Bx_fciLik_25' , 'w1Bx_fciLik_16' , 'w1Bx_fciLik_24' , 'w1Bx_fciLik_17' , 'w1Bx_fciLik_23' , 'w1Bx_fciLik_1' , 'w1Bx_fciLik_8' , 'w1Bx_fciLik_13']].mean()

            fci_lc=fciLik_df.loc[bbx_id,['w1Bx_fciLik_21' , 'w1Bx_fciLik_18' , 'w1Bx_fciLik_12' , 'w1Bx_fciLik_5' , 'w1Bx_fciLik_9' , 'w1Bx_fciLik_28' , 'w1Bx_fciLik_14' , 'w1Bx_fciLik_22']].mean()

            fci_lff=fciLik_df.loc[bbx_id,['w1Bx_fciLik_11' , 'w1Bx_fciLik_7' , 'w1Bx_fciLik_20' , 'w1Bx_fciLik_2']].mean()

            
        except:
            error_ids.append(bbx_id)

        # set dictionary
        if bbx_id not in fci_dict:
            fci_dict[bbx_id]={}

        # add values to dictionary
        fci_dict[bbx_id]["w1fci_crave"]=fci_crave
        fci_dict[bbx_id]["w1fci_chf"]=fci_chf
        fci_dict[bbx_id]["w1fci_cs"]=fci_cs
        fci_dict[bbx_id]["w1fci_cc"]=fci_cc
        fci_dict[bbx_id]["w1fci_cff"]=fci_cff	
        fci_dict[bbx_id]["w1fci_like"]=fci_like
        fci_dict[bbx_id]["w1fci_lhf"]=fci_lhf
        fci_dict[bbx_id]["w1fci_ls"]=fci_ls
        fci_dict[bbx_id]["w1fci_lc"]=fci_lc	
        fci_dict[bbx_id]["w1fci_lff"]=fci_lff
        
        

    if not error_ids:
        pass
    else:
        print("\n[INFO] ERROR with FCI calculation for ids: ",set(error_ids))
    
    # make dataframe 
    
    df_final= pd.DataFrame(fci_dict).T  
    display(df_final.tail())
    
    df_final.to_csv(os.path.join(output_path, "w1Bx_fci_calculations.csv"))
    print('\n[INFO] completed FCI calculations.\n')
    
    
    return df_final;





def debq_calculation():
    # set starting variables
    debq_dict={}
    error_ids=[]
    s1_behav_copy=s1_behav        

    """
    # Reverse Scoring 
    """
    s1_behav_copy["w1Bx_debq_33"] = s1_behav_copy["w1Bx_debq_33"].replace(['5','4','3','2','1'], ['1','2','3','4','5'])  
    
    
    
    
    debq_df=s1_behav_copy.filter(like="debq", axis=1)
    debq_df=debq_df.apply(pd.to_numeric,  errors='coerce')
   
    #display(debq_df.head())
    
    """
    # Calculations
    """

    for bbx_id in s1_behav.index.values:
        try:

            debq_tot=debq_df.loc[bbx_id, :].mean()
            debq_r=debq_df.loc[bbx_id, ['w1Bx_debq_1' , 'w1Bx_debq_2' , 'w1Bx_debq_3' , 'w1Bx_debq_4' , 'w1Bx_debq_5' , 'w1Bx_debq_6' , 'w1Bx_debq_7' , 'w1Bx_debq_8' , 'w1Bx_debq_9' , 'w1Bx_debq_10']].mean()
            debq_e=debq_df.loc[bbx_id, ['w1Bx_debq_11' , 'w1Bx_debq_12' , 'w1Bx_debq_13' , 'w1Bx_debq_14' , 'w1Bx_debq_15' , 'w1Bx_debq_16' , 'w1Bx_debq_17',
                                        'w1Bx_debq_18' , 'w1Bx_debq_19' , 'w1Bx_debq_20' , 'w1Bx_debq_21' , 'w1Bx_debq_22' , 'w1Bx_debq_23']].mean()
            debq_ext=debq_df.loc[bbx_id, ['w1Bx_debq_24' , 'w1Bx_debq_25' , 'w1Bx_debq_26' , 'w1Bx_debq_27' , 'w1Bx_debq_28' , 'w1Bx_debq_29' , 'w1Bx_debq_30' , 'w1Bx_debq_31' , 'w1Bx_debq_32' , 'w1Bx_debq_33']].mean()



            # set dictionary
            if bbx_id not in debq_dict:
                debq_dict[bbx_id]={}

            # add values to dictionary
            debq_dict[bbx_id]["w1debq_tot"]=debq_tot
            debq_dict[bbx_id]["w1debq_r"]=debq_r
            debq_dict[bbx_id]["w1debq_e"]=debq_e
            debq_dict[bbx_id]["w1debq_ext"]=debq_ext
        except:
            error_ids.append(bbx_id)
        
    if not error_ids:
        pass
    else:
        print("\n[INFO] ERROR with DEBQ calculation for ids: ",set(error_ids))
    
    # make dataframe 
    
    df_final= pd.DataFrame(debq_dict).T  
    display(df_final.tail())
    
    df_final.to_csv(os.path.join(output_path, "w1Bx_debq_calculations.csv"))
    print('\n[INFO] completed DEBQ calculations.\n')
    
    
    return df_final;
        
    
    
def spsrq_calculation():
    # set starting variables
    spsrq_dict={}
    error_ids=[]
    s1_behav_copy=s1_behav        
    
    spsrq_df=s1_behav_copy.filter(like="spsrq", axis=1)
    spsrq_df=spsrq_df.apply(pd.to_numeric,  errors='coerce')
   
    #display(spsrq_df.head())
    
    """
    # Calculations
    """

    for bbx_id in s1_behav.index.values:
        try:
            spsrq_tot=sum(spsrq_df.loc[bbx_id, ['w1Bx_spsrq1' , 'w1Bx_spsrq2' , 'w1Bx_spsrq3' , 'w1Bx_spsrq4' , 'w1Bx_spsrq5' , 'w1Bx_spsrq6' , 'w1Bx_spsrq7' ,
                                                'w1Bx_spsrq8' , 'w1Bx_spsrq9' , 'w1Bx_spsrq10' , 'w1Bx_spsrq11' , 'w1Bx_spsrq12' , 'w1Bx_spsrq13' , 'w1Bx_spsrq14' , 'w1Bx_spsrq15' ,
                                                'w1Bx_spsrq16' , 'w1Bx_spsrq17' , 'w1Bx_spsrq18' , 'w1Bx_spsrq19' , 'w1Bx_spsrq20']])

            spsrq_sp=sum(spsrq_df.loc[bbx_id, ['w1Bx_spsrq1' , 'w1Bx_spsrq3' , 'w1Bx_spsrq5' , 'w1Bx_spsrq7' , 'w1Bx_spsrq9' , 'w1Bx_spsrq11' , 'w1Bx_spsrq13' , 'w1Bx_spsrq15' , 'w1Bx_spsrq17' , 'w1Bx_spsrq19']])

            spsrq_sr=sum(spsrq_df.loc[bbx_id, ['w1Bx_spsrq2' , 'w1Bx_spsrq4' , 'w1Bx_spsrq6' , 'w1Bx_spsrq8' , 'w1Bx_spsrq10' , 'w1Bx_spsrq12' , 'w1Bx_spsrq14' , 'w1Bx_spsrq16' , 'w1Bx_spsrq18' , 'w1Bx_spsrq20']])
        except:
            error_ids.append(bbx_id)
        # set dictionary
        if bbx_id not in spsrq_dict:
            spsrq_dict[bbx_id]={}

        # add values to dictionary
        spsrq_dict[bbx_id]["w1spsrq_tot"]=spsrq_tot
        spsrq_dict[bbx_id]["w1spsrq_sp"]=spsrq_sp
        spsrq_dict[bbx_id]["w1spsrq_sr"]=spsrq_sr
      
        
    if not error_ids:
        pass
    else:
        print("\n[INFO] ERROR with SPSRQ calculation for ids: ",set(error_ids))
    
    # make dataframe 
    
    df_final= pd.DataFrame(spsrq_dict).T  
    display(df_final.tail())
    
    df_final.to_csv(os.path.join(output_path, "w1Bx_spsrq_calculations.csv"))
    print('\n[INFO] completed SPSRQ calculations.\n')
    
    
    return df_final;
 
    
    
    

def bis_bas_calculation():
    # set starting variables
    bbas_dict={}
    error_ids=[]
    s1_behav_copy=s1_behav        
   
    #display(spsrq_df.head())
    """
    # Reverse Scoring 
    """
    
    #display(s1_behav_copy.filter(like="bis_bas", axis=1).head())
    
    cols=["w1Bx_bis_bas_1", 'w1Bx_bis_bas_3', 'w1Bx_bis_bas_4' , 'w1Bx_bis_bas_5', 'w1Bx_bis_bas_6', 'w1Bx_bis_bas_7', 'w1Bx_bis_bas_8', 
          'w1Bx_bis_bas_9', 'w1Bx_bis_bas_10', 'w1Bx_bis_bas_11', 'w1Bx_bis_bas_12', 'w1Bx_bis_bas_13', 'w1Bx_bis_bas_14', 'w1Bx_bis_bas_15', 'w1Bx_bis_bas_16', 
          'w1Bx_bis_bas_17', 'w1Bx_bis_bas_18', 'w1Bx_bis_bas_19', 'w1Bx_bis_bas_20', 'w1Bx_bis_bas_22', 'w1Bx_bis_bas_23']
    
    s1_behav_copy[cols]= s1_behav_copy[cols].replace(['4','3','2','1'], ['1','2','3','4'])
    
    #display(s1_behav_copy.filter(like="bis_bas", axis=1).head())
    
    bbas_df=s1_behav_copy.filter(like="bis_bas", axis=1)
    bbas_df=bbas_df.apply(pd.to_numeric,  errors='coerce')

    """
    # Calculations
    """
    
    for bbx_id in s1_behav.index.values:
        try:
            bisbas_bastot=sum(bbas_df.loc[bbx_id, ['w1Bx_bis_bas_3' , 'w1Bx_bis_bas_8' , 'w1Bx_bis_bas_11' , 'w1Bx_bis_bas_20',
                                                    'w1Bx_bis_bas_5' , 'w1Bx_bis_bas_9' , 'w1Bx_bis_bas_14' , 'w1Bx_bis_bas_19', 'w1Bx_bis_bas_4',
                                                    'w1Bx_bis_bas_6' , 'w1Bx_bis_bas_13' , 'w1Bx_bis_bas_17' , 'w1Bx_bis_bas_22']])

            bisbas_basd=sum(bbas_df.loc[bbx_id, ['w1Bx_bis_bas_3' , 'w1Bx_bis_bas_8' , 'w1Bx_bis_bas_11' , 'w1Bx_bis_bas_20']])

            bisbas_basfs=sum(bbas_df.loc[bbx_id, ['w1Bx_bis_bas_5' , 'w1Bx_bis_bas_9' , 'w1Bx_bis_bas_14' , 'w1Bx_bis_bas_19']])

            bisbas_basrr=sum(bbas_df.loc[bbx_id, ['w1Bx_bis_bas_4' , 'w1Bx_bis_bas_6' , 'w1Bx_bis_bas_13' , 'w1Bx_bis_bas_17' , 'w1Bx_bis_bas_22']])

            bisbas_bis=sum(bbas_df.loc[bbx_id, ['w1Bx_bis_bas_2' , 'w1Bx_bis_bas_7' , 'w1Bx_bis_bas_12' , 'w1Bx_bis_bas_15' , 'w1Bx_bis_bas_18' , 'w1Bx_bis_bas_21' , 'w1Bx_bis_bas_23']])
        except:
            error_ids.append(bbx_id)
        # set dictionary
        if bbx_id not in bbas_dict:
            bbas_dict[bbx_id]={}

        # add values to dictionary
        bbas_dict[bbx_id]["w1bisbas_bastot"]=bisbas_bastot
        bbas_dict[bbx_id]["w1bisbas_basd"]=bisbas_basd
        bbas_dict[bbx_id]["w1bisbas_basfs"]=bisbas_basfs
        bbas_dict[bbx_id]["w1bisbas_basrr"]=bisbas_basrr
        bbas_dict[bbx_id]["w1bisbas_bis"]=bisbas_bis
        
    if not error_ids:
        pass
    else:
        print("\n[INFO] ERROR with BIS/BAS calculation for ids: ",set(error_ids))
    
    # make dataframe 
    
    df_final= pd.DataFrame(bbas_dict).T  
    display(df_final.tail())
    
    df_final.to_csv(os.path.join(output_path, "w1Bx_bis_bas_calculations.csv"))
    print('\n[INFO] completed BIS/BAS calculations.\n')
    
    
    return df_final;




def pfs_calculation():
    # set starting variables
    pfs_dict={}
    error_ids=[]
    s1_behav_copy=s1_behav        
        
    pfs_df=s1_behav_copy.filter(like="pfs", axis=1)
    pfs_df=pfs_df.apply(pd.to_numeric,  errors='coerce')

    """
    # Calculations
    """
    
    for bbx_id in s1_behav.index.values:
        try:
            pfs_tot=pfs_df.loc[bbx_id, ['w1Bx_pfs_1' , 'w1Bx_pfs_3' , 'w1Bx_pfs_8' , 'w1Bx_pfs_16' , 'w1Bx_pfs_17' , 'w1Bx_pfs_19', 'w1Bx_pfs_5' , 'w1Bx_pfs_6' , 
                                                 'w1Bx_pfs_10' , 'w1Bx_pfs_11', 'w1Bx_pfs_14' , 'w1Bx_pfs_15' , 'w1Bx_pfs_18' , 'w1Bx_pfs_20' , 'w1Bx_pfs_21']].mean()

            pfs_fa=pfs_df.loc[bbx_id, ['w1Bx_pfs_1' , 'w1Bx_pfs_3' , 'w1Bx_pfs_8' , 'w1Bx_pfs_16' , 'w1Bx_pfs_17' , 'w1Bx_pfs_19']].mean()
            pfs_fp=pfs_df.loc[bbx_id, ['w1Bx_pfs_5' , 'w1Bx_pfs_6' , 'w1Bx_pfs_10' , 'w1Bx_pfs_11']].mean()
            pfs_ft=pfs_df.loc[bbx_id, ['w1Bx_pfs_14' , 'w1Bx_pfs_15' , 'w1Bx_pfs_18' , 'w1Bx_pfs_20' , 'w1Bx_pfs_21']].mean()

        except:
            error_ids.append(bbx_id)
            
        # set dictionary
        if bbx_id not in pfs_dict:
            pfs_dict[bbx_id]={}

        # add values to dictionary
        pfs_dict[bbx_id]["w1pfs_tot"]=pfs_tot
        pfs_dict[bbx_id]["w1pfs_fa"]=pfs_fa
        pfs_dict[bbx_id]["w1pfs_fp"]=pfs_fp
        pfs_dict[bbx_id]["w1pfs_ft"]=pfs_ft
        
    if not error_ids:
        pass
    else:
        print("\n[INFO] ERROR with PFS calculation for ids: ",set(error_ids))
    
    # make dataframe 
    
    df_final= pd.DataFrame(pfs_dict).T  
    display(df_final.tail())
    
    #df_final.to_csv(os.path.join(output_path, "w1Bx_pfs_calculations.csv"))
    print('\n[INFO] completed PFS calculations.\n')
    
    
    return df_final;
        
    
    
    
def yfas_calculation():
    # set starting variables
    yfas_dict={}
    error_ids=[]
    s1_behav_copy=s1_behav        
    sess_id="w1"
    #display(spsrq_df.head())
    """
    # Reverse Scoring 
    """
    
    #display(s1_behav_copy.filter(like="yfas", axis=1).head())
    cols1=['w1Bx_yfas_1' , 'w1Bx_yfas_2' , 'w1Bx_yfas_4' , 'w1Bx_yfas_6', 'w1Bx_yfas_3',
           'w1Bx_yfas_5', 'w1Bx_yfas_7' , 'w1Bx_yfas_9' , 'w1Bx_yfas_12' , 
           'w1Bx_yfas_13', 'w1Bx_yfas_14', 'w1Bx_yfas_15', 'w1Bx_yfas_16']
    s1_behav_copy[cols1]= s1_behav_copy[cols1].replace(['1','2','3','4'], ['0','0','0','1'])
    
    cols2=[ 'w1Bx_yfas_8', 'w1Bx_yfas_10', 'w1Bx_yfas_11']
    s1_behav_copy[cols2]= s1_behav_copy[cols2].replace(['1','2','3','4'], ['0','0','1','1'])
    
    cols3=['w1Bx_yfas_17_3', 'w1Bx_yfas_17_4', 'w1Bx_yfas_17_5', 'w1Bx_yfas_17_6']
    s1_behav_copy[cols3]= s1_behav_copy[cols3].replace(['1','2'], ['0','1'])
    
    s1_behav_copy['w1Bx_yfas_17_8']= s1_behav_copy['w1Bx_yfas_17_8'].replace(['2'], ['0'])
    
    s1_behav_copy['w1Bx_yfas_25']= s1_behav_copy['w1Bx_yfas_25'].replace(['1','2', '3', '4', '5'], ['0', '0', '0', '0', '1'])
    
    #display(s1_behav_copy.filter(like="yfas", axis=1).head())

    
    yfas_df=s1_behav_copy.filter(like="yfas", axis=1)
    yfas_df=yfas_df.apply(pd.to_numeric,  errors='coerce')

    #display(yfas_df.head())
    
    """
    # Calculations
    """
    
    for bbx_id in s1_behav.index.values:
        try:
            yfas_c1=sum(yfas_df.loc[bbx_id, ['%sBx_yfas_1'%sess_id , '%sBx_yfas_2'%sess_id , '%sBx_yfas_3'%sess_id]])

            yfas_c2=sum(yfas_df.loc[bbx_id, ['%sBx_yfas_4'%sess_id , '%sBx_yfas_17_6'%sess_id , '%sBx_yfas_17_8'%sess_id,
                                            '%sBx_yfas_25'%sess_id]])
            yfas_c3=sum(yfas_df.loc[bbx_id, ['%sBx_yfas_5'%sess_id , '%sBx_yfas_6'%sess_id , '%sBx_yfas_7'%sess_id]])

            yfas_c4=sum(yfas_df.loc[bbx_id, ['%sBx_yfas_8'%sess_id , '%sBx_yfas_9'%sess_id , '%sBx_yfas_10'%sess_id,
                                            '%sBx_yfas_11'%sess_id ]])

            yfas_c5=float(yfas_df.loc[bbx_id, ['%sBx_yfas_17_3'%sess_id ]])

            yfas_c6=sum(yfas_df.loc[bbx_id, ['%sBx_yfas_17_4'%sess_id, '%sBx_yfas_17_5'%sess_id]])

            yfas_c7=sum(yfas_df.loc[bbx_id, ['%sBx_yfas_12'%sess_id, '%sBx_yfas_13'%sess_id, '%sBx_yfas_14'%sess_id ]])

            yfas_c8=sum(yfas_df.loc[bbx_id, ['%sBx_yfas_15'%sess_id, '%sBx_yfas_16'%sess_id]])

            #print(yfas_df.loc[bbx_id, ['%sBx_yfas_15'%sess_id, '%sBx_yfas_16'%sess_id]])
            #print(yfas_c1, yfas_c2, yfas_c3, yfas_c4, yfas_c5,yfas_c6,yfas_c7,yfas_c8)

            if yfas_c1 == 0:
                yfas_c1_met=0
            elif yfas_c1 >=1 :
                yfas_c1_met=1
            else:
                pass

            if yfas_c2 == 0:
                yfas_c2_met=0
            elif yfas_c2 >= 1:
                yfas_c2_met=1

            if yfas_c3 == 0:
                yfas_c3_met=0
            elif yfas_c3 >= 1:
                yfas_c3_met=1

            if yfas_c4 == 0:
                yfas_c4_met=0
            elif yfas_c4 >= 1:
                yfas_c4_met=1

            if yfas_c5 == 0:
                yfas_c5_met=0
            elif yfas_c5 >= 1:
                yfas_c5_met=1

            if yfas_c6 == 0:
                yfas_c6_met=0
            elif yfas_c26 >= 1:
                yfas_c6_met=1


            if yfas_c7 == 0:
                yfas_c7_met=0
            elif yfas_c7 >= 1:
                yfas_c7_met=1

            if yfas_c8 == 0:
                yfas_c8_met=0
            elif 8 >= 1:
                yfas_c8=met=1

            yfas_cont_score=yfas_c1_met+yfas_c2_met+yfas_c3_met+yfas_c4_met+yfas_c5_met+yfas_c6_met+yfas_c7_met+yfas_c8_met
            #print(yfas_cont_score)

        except:
            error_ids.append(bbx_id)
            
        # set dictionary
        if bbx_id not in yfas_dict:
            yfas_dict[bbx_id]={}

        # add values to dictionary
        yfas_dict[bbx_id]["%syfas_c1"%sess_id]=yfas_c1
        yfas_dict[bbx_id]["%syfas_c2"%sess_id]=yfas_c2
        yfas_dict[bbx_id]["%syfas_c3"%sess_id]=yfas_c3
        yfas_dict[bbx_id]["%syfas_c4"%sess_id]=yfas_c4
        yfas_dict[bbx_id]["%syfas_c5"%sess_id]=yfas_c5
        yfas_dict[bbx_id]["%syfas_c6"%sess_id]=yfas_c6
        yfas_dict[bbx_id]["%syfas_c7"%sess_id]=yfas_c7
        yfas_dict[bbx_id]["%syfas_c8"%sess_id]=yfas_c8
        yfas_dict[bbx_id]["%syfas_c1_met"%sess_id]=yfas_c1_met
        yfas_dict[bbx_id]["%syfas_c2_met"%sess_id]=yfas_c2_met
        yfas_dict[bbx_id]["%syfas_c3_met"%sess_id]=yfas_c3_met
        yfas_dict[bbx_id]["%syfas_c4_met"%sess_id]=yfas_c4_met
        yfas_dict[bbx_id]["%syfas_c5_met"%sess_id]=yfas_c5_met
        yfas_dict[bbx_id]["%syfas_c6_met"%sess_id]=yfas_c6_met
        yfas_dict[bbx_id]["%syfas_c7_met"%sess_id]=yfas_c7_met
        yfas_dict[bbx_id]["%syfas_c8_met"%sess_id]=yfas_c8_met
        yfas_dict[bbx_id]["%syfas_cont_score"%sess_id]=yfas_cont_score
        
        
    if not error_ids:
        pass
    else:
        print("\n[INFO] ERROR with YFAS calculation for ids: ",set(error_ids))
    
    # make dataframe 
    
    df_final= pd.DataFrame(yfas_dict).T  
    display(df_final.tail(20))
    
    df_final.to_csv(os.path.join(output_path, "w1Bx_yfas_calculations.csv"))
    print('\n[INFO] completed YFAS calculations.\n')
 