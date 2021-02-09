"""
Name       : Chethan Singh Mysore Jagadeesh
Class      : METCS-521 Summer 1 online 2018
Date       : Mon Jun 18 19:38:05 2018
Assignment : FINAL PROJECT - TV ADVERTISING RECOMMENDATION TOOL
Description: TV ADVERTISING RECOMMENDATION TOOL
"""
import os
import fnmatch
import datetime
import math

def initail_setup() :
    """
      Initail Variable setup
      
    """
    
    ##Create a global dictionary for wide traffic system dayparts
    global daypart_dict
    daypart_dict = { "1" : { "Name":"M-F 5A-4P",
                             "Description" : "Monday to Friday 5AM to 4PM",
                        "StartDoW" : 0,
                        "EndDoW" : 4,
                        "StartTime" : "0500",
                        "EndTime":"1559"
                       },
                       
                "2" : { "Name":"M-F 4P-12M",
                        "Description" : "Monday to Friday 4PM to 12Midnight",
                        "StartDoW" : 0,
                        "EndDoW" : 4,
                        "StartTime" : "1600",
                        "EndTime":"2359"
                       },

                "3" : { "Name":"Sa-Su 5A-4P",
                        "Description" : "Saturday and Sunday 5AM to 4PM",
                        "StartDoW" : 5,
                        "EndDoW" : 6,
                        "StartTime" : "0500",
                        "EndTime":"1559"
                       },
                       
                "4" : { "Name":"Sa-Su 4P-12M",
                        "Description" : "Saturday and Sunday 4PM to 12Midnight",
                        "StartDoW" : 5,
                        "EndDoW" : 6,
                        "StartTime" : "1600",
                        "EndTime":"2359"
                       }
              }

    ##Create a global dictionary for target audience of TV ad   
    global audience_dict    
    audience_dict ={"1" : "Households",
		"2" : "Children 2 to 5 years",
		"3" : "Children 6 to 11 years",
		"4" : "Male 12 to 20 years",
		"5" : "Male 21 to 33 years",
		"6" : "Male 34 to 54 years",
		"7" : "Male 55Plus years",
		"8" : "Wpmen 12 to 20 years",
		"9" : "Women 21 to 34 years",
		"10" : "Wowen 34 to 54 years",
		"11" : "Women 55Plus years" }
  
    ##Create a global dictionary for list of zones for which currently data available
    global zone_dict
    zone_dict = {"1" : "Clayton",
             "2" : "Douglas",
             "3" : "TestZone"}

    ##Create a global dictionary for list of networks for which currently data available
    global network_dict             
    network_dict = {"1" : "CNN",
                    "2" : "FXN",
                    "3" : "HGTV",
                    "4" : "FOOD",
                    "5" : "ESPN"}
    
    ##Create a global dictionary for list of broadcastweeks for which currently data available                
    global bcastWeek_dict              
    bcastWeek_dict = {"1" : "40",
                  "2" : "41"}
    
    ####Create a global dictionary for list of options available on audience forecast page
    global forecastAudienceOptions_dict             
    forecastAudienceOptions_dict = {"1": "Forecast for a new TV advertising spot",
                                "2": "List saved forecasts"}
    ####Create a global dictionary for list of options available on recommendation page
    global recommendationOptions_dict
    recommendationOptions_dict = {"1": "Get New Recommendation",
                              "2": "View a Saved Recommendation"}
    
    ### Create a global list to all the previous forecast requests in a given session
    ### this avoids accessing data sets if previous request has to be reviewed
    global tvOrderForecast_list              
    tvOrderForecast_list = list()
    
    ### Create a global list to all the previous recommendations requests in a given session
    ### this avoids accessing data sets if previous request has to be reviewed
    global recommendation_list
    recommendation_list = list()


class TVAdOrder :
    """
      TVAdOrder class represents a typical TV ADVERTSING SPOT order on a traffic system
      with variables:Network , target zone, target audience, daypart, broadcast week
      with methods : to calculate impressions forecast and spotprice      
    """
    
    def __init__(self, orderId, network, zoneName, broadcastWeek, targetAudience, daypart, dataFile):
        self.__orderId = orderId        
        self.__network = network
        self.__zoneName = zoneName
        self.__broadcastWeek = broadcastWeek
        self.__targetAudience = targetAudience
        self.__daypart = daypart
        self.__dataFile = dataFile
        self.setDaypart(daypart)
        self.__setImpressionsAndPrice()
        
    def __repr__(self) :
        return "TVAdOrder"+str(self.__orderId)
        
    def setOrderId(self, orderId) :
        self.__orderId = orderId
        
    def getOrderId(self) :
        return self.__orderId

    def setNetwork(self, network) :
        self.__network = network
        
    def getNetwork(self) :
        return self.__network
        
    def setZoneName(self, zoneName) :
        self.__zoneName = zoneName
        
    def getZoneName(self) :
        return self.__zoneName
        
    def setBroadcastWeek(self, broadcastWeek) :
        self.__broadcastWeek = broadcastWeek
        
    def getBroadcastWeek(self) :
        return self.__broadcastWeek
     
    def setTargetAudience(self, targetAudience) :
        self.__targetAudience = targetAudience
        
    def getTargetAudience(self) :
        return audience_dict[str(self.__targetAudience)]
        
    def setDaypart(self, daypart) :
        self.__daypart = daypart
        self.__setStartDoW()
        self.__setEndDoW()
        self.__setStartTime()
        self.__setEndTime()
        
    def getDaypartName(self) :
        return self.__daypart["Name"]
        
    def __setStartDoW(self) :
        self.__startDoW = self.__daypart["StartDoW"]
        
    def __getStartDoW(self) :
        return self.__startDoW
        
    def __setEndDoW(self) :
        self.__endDoW = self.__daypart["EndDoW"]
        
    def __getEndDoW(self) :
        return self.__endDoW
        
    def __setStartTime(self) :
        self.__startTime = self.__daypart["StartTime"]
        
    def __getStartTime(self) :
        return self.__startTime
        
    def __setEndTime(self) :
        self.__endTime = self.__daypart["EndTime"]
        
    def __getEndTime(self) :
        return self.__endTime
        
    def setDataFile(self, dataFile) :
        self.__dataFile = dataFile
        
      
    def __setImpressionsAndPrice(self):
        
        """
        Set Impressions forecast and Spotprice based on previous 4 years of data
        """
        
        ##Create an empty list to hold impressions for each of past 4 years
        yearlyImpression_list = list()
        
        ##Create an empty list to hold spotprice for each of past 4 years
        yearlySpotPrice_list = list()
        
        ##define a weightage list for data derived for past 4 yeras
        ##for a impression forecast of a spot in 2018
        ## 2017 data gets weightage of 5
        ## 2016 af 3
        ## 2015 of 2
        ## 2015 of 1
        ## in the final average of past 4 yeras of data
        ## this will ensure current years forecast is as close to average values of previous year
        weightage_list = [5,3,2,1]        
        
        
        ###for each of the file for past 4 years calculet teh spotprice and impressions for the selected spot
        for file_name in self.__dataFile:
            
            ## Open file for reading
            infile = open(file_name,"r")

            ##read line 1
            line=infile.readline()
        
            ##Create empty list to hold impression values from each line matching the order criteria 
            impression_list = list()
            
            ##Create empty list to hold impression values from each line matching the order criteria 
            spotPrice_list = list()         
            
            ## for each line in given file do the following
            while line != '' :
                
                line=infile.readline()
                
                ##Split the file into list of strings as input file is pipe delimited
                column_value_list = line.split('|')
                
                ## if end of file is reached then close the file and continue with next file
                if len(column_value_list) < 2 :
                    
                    infile.close()
                    break
                
                ##Conevert teh string in 4 column of the list into date which is broadcast date for which neilsen has provided data for
                bcastdate = datetime.datetime(int(column_value_list[3].split('-')[0]), int(column_value_list[3].split('-')[1]), int(column_value_list[3].split('-')[2]))
                
                ## Get the year of the data                 
                data_year = int(column_value_list[3].split('-')[0])
                
                ##For each line read, fileter the matching records
                ##filter based on network selected
                ## filter based on start day of week and end day of week of the daypart selected
                ## filter based on start time and end time of the daypart selected
                
                if self.__network == column_value_list[2] and \
                    bcastdate.weekday() >= self.__getStartDoW() and bcastdate.weekday() <= self.__getEndDoW() and \
                    int(column_value_list[5]) >= int(self.__getStartTime()) and int(column_value_list[5]) < int(self.__getEndTime()):   
                        
                        ## based on the target audience selected get the impression value givenby neilsen files
                        ## Note that impresison values for various audience starts from column 8 0r index of 7
                        impression_list.append(float(column_value_list[self.__targetAudience + 6]))
                        
                        ## based on the target audience selected get the cost per 1000 HHImp values givenby neilsen files
                        ## Note that 'cost per 1000 HHImp' values is at column 7 0r index of 6
                        ##spotprice = 'cost per 1000 HHImp' * HHImp(column 8 or index 7) divided by 1000.0
                        spotPrice_list.append((float(column_value_list[6]) * float(column_value_list[7]))/1000.0)
                        
                        
        
            ## Sort the matching list of impression values for the selected target audience
            impression_list.sort()
            
            ## Sort the matching list of spotprice calculated for the given order
            spotPrice_list.sort()
            

            ## to eleiminate the extereme values in the in the list to get theaverage value for each year
            ## eliminate data in bottom 20 percentile and top 20 percentile before getting the average value for each year
            twently_percentile_count =  math.floor(len(impression_list)*0.2)
            
            ## if there are less number of elments from which 40% f records cannot be eliminated then retain al records
            if twently_percentile_count < 2 : 
                sixty_percentile_impression_list = impression_list[:]
                sixty_percentile_spotPrice_list = spotPrice_list[:]
            
            else : ## eliminate bottom and top 20 percentile
                sixty_percentile_impression_list = impression_list[twently_percentile_count : -twently_percentile_count]
                sixty_percentile_spotPrice_list = spotPrice_list[twently_percentile_count : -twently_percentile_count]
        
            
            ## Set impression and spotprice as zero if there is no enough data to support
            if len(sixty_percentile_impression_list) == 0 :
                impressions = 0
                spotPrice = 0
            else :           
                ## return average impressions
                assert (len(sixty_percentile_impression_list) > 0 ) , "Data not available to calculate impressions"
                impressions =  (sum(sixty_percentile_impression_list) / len(sixty_percentile_impression_list))
                spotPrice = (sum(sixty_percentile_spotPrice_list) / len(sixty_percentile_spotPrice_list))
                ##print(file_name,": ",impressions, ": ",spotPrice )
                
            ## get the current year for which spot is palced and trying to forecast the impression and spotprice    
            now = datetime.datetime.now()
            this_year = int(now.year)
            
            ## dependiening the data availability of each year set the weightage
            ## so that, if data not available then that particular years data is not considered in the final weighted average 
            if data_year ==  (this_year - 1) : 
                yearlyImpression_list.append(impressions * 5)
                yearlySpotPrice_list.append(spotPrice * 5)
                if impressions == 0 : weightage_list[0] = 0
                
            elif  data_year ==  (this_year - 2) : 
                yearlyImpression_list.append(impressions * 3)
                yearlySpotPrice_list.append(spotPrice * 3)
                if impressions == 0 : weightage_list[1] = 0
                
            elif  data_year ==  (this_year - 3) : 
                yearlyImpression_list.append(impressions * 2)
                yearlySpotPrice_list.append(spotPrice * 2)
                if impressions == 0 : weightage_list[2] = 0
                
            elif  data_year ==  (this_year - 4) : 
                yearlyImpression_list.append(impressions * 1)
                yearlySpotPrice_list.append(spotPrice * 1)
                if impressions == 0 : weightage_list[3] = 0
                
            
                        
        if sum(weightage_list) == 0 :
            self.__impressions = 0
            self.__spotPrice = 0
        else :
            ##get weighted average of impression and spotprice values for past 4 years
            self.__impressions = math.floor(sum(yearlyImpression_list)/sum(weightage_list))
            self.__spotPrice = math.ceil(sum(yearlySpotPrice_list)/sum(weightage_list))
        
    def getImpressions(self):
        return self.__impressions

    def getSpotPrice(self) :
        return self.__spotPrice





def validChoice(dictionary, input_name, currentChoice_dict, print_choices=True):
    
    """
       Function to display the valid options to choose from dynamically and
       validate user entered option
       
    """
        
    if print_choices :
        for keys in dictionary:
            print(keys,". ",dictionary[keys])
            
        
    while True:
        try:
            
            print("\nEnter Number listed above against your choice :")
            choice = str(input()).strip()
        
            if choice not in [keys for keys in dictionary ] : raise ValueError
                
        except ValueError :
            print("\nInvalid ", input_name," Choice!! TRY AGAIN!!")
            continue
        
        break
    
    ##Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    currentChoice_dict[input_name] = dictionary[choice]
    
  
    for criteria, value in currentChoice_dict.items():
        
        if criteria == "Page" : print("\n\n\n                                      ",value,"\n\n")
        elif  criteria == "Daypart" : print("\n","{:<50s}".format("     selected "+  criteria)," : ",value["Name"])
        else : print("\n","{:<50s}".format("     Selected "+ criteria)," : ",value)
        
    return choice


def continue_function():
    
    print("\n\n PRESS ENTER TO CONTINUE..........")
        
    try:
        input()
        
    except SyntaxError:
        return 0
            

    

def forecastAudience():
    
    #####Audience forecast page for teh specific spot selected by the user by entering
    #####Network, daypart, bcast week, zone and target audience
    
    currentChoice_dict= dict()    
    currentChoice_dict["Page"] = "--------------------FORECAST AUDIENCE------------------------"
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\n\n                                      ",currentChoice_dict["Page"],"\n\n")
    print("\nSelect one of the following ")
    forecastAudienceOption_choice=validChoice(forecastAudienceOptions_dict, "Forecast Audience Option",currentChoice_dict)
   
    
    #### Display the previously saved forecasts
    if forecastAudienceOption_choice == "2" :
       if len(tvOrderForecast_list) == 0 :
           print("\n\nNO SAVED FORECASTS!!!")
           continue_function()
           return 0
           
       else:
           print("\n\n","{:<12s}".format("OrderID"),"{:<12s}".format("Network"),"{:<12s}".format("Zone"),"{:<15s}".format("Daypart"),"{:<28s}".format("TargetAudience"),"{:<15s}".format("BroadcastWeek"),"|","{:<22s}".format("Viewers Estimate"),"{:<25s}".format("SpotPrice Estimate"))
           print("--------------------------------------------------------------------------------------------------------------------------------------")
           for tvAdOrder in tvOrderForecast_list :
              
              if tvAdOrder.getImpressions() > 0:
                  print("{:<13s}".format(" "+str(tvAdOrder.getOrderId())),"{:<12s}".format(str(tvAdOrder.getNetwork())),"{:<12s}".format(str(tvAdOrder.getZoneName())),\
                  "{:<15s}".format(str(tvAdOrder.getDaypartName())),"{:<28s}".format(str(tvAdOrder.getTargetAudience())),\
                  "{:<15s}".format(str(tvAdOrder.getBroadcastWeek())),"|","{:<22s}".format(str(tvAdOrder.getImpressions())),"{:<25s}".format(str(tvAdOrder.getSpotPrice())))
              else :
                  print("{:<13s}".format(" "+str(tvAdOrder.getOrderId())),"{:<12s}".format(str(tvAdOrder.getNetwork())),"{:<12s}".format(str(tvAdOrder.getZoneName())),\
                  "{:<15s}".format(str(tvAdOrder.getDaypartName())),"{:<28s}".format(str(tvAdOrder.getTargetAudience())),\
                  "{:<15s}".format(str(tvAdOrder.getBroadcastWeek())),"| NO FORECAST AVAILABLE DUE TO LACK OF DATA",)
           
           continue_function()
           return 0
           

    ### if the user has opted for get forecast for new spot then do the following
    print("\nSelect target geographical zone for your TV ad spot")
          
    zone_choice = validChoice(zone_dict,"Zone",currentChoice_dict)
    
   
    
    print("\nSelect Target Audience for your TV ad spot")
    
    audience_choice = validChoice(audience_dict,"Audience",currentChoice_dict)
    
           
            
    print("\nSelect Network for your TV ad spot")
    
    network_choice = validChoice(network_dict,"Network",currentChoice_dict)
    
   
    
    print("\nSelect Broadcast Week of year 2018 when you want to air your TV ad")
    
    bcastWeek_choice = validChoice(bcastWeek_dict,"Broadcast Week",currentChoice_dict)
    
   
    
    print("\nSelect Daypart during which you are targeting to air your TV ad")
    
    for keys in daypart_dict:
        print(keys,". ",daypart_dict[keys]["Name"]," - ", daypart_dict[keys]["Description"])
    
    daypart_choice = validChoice(daypart_dict,"Daypart",currentChoice_dict,False)
    

    ##### Narrow down the files from which the relevant data is filetred baed on user entered spot details
    ##### File name format is    NielsenImpression_{zone}_{broadcastweek}_{year}.txt
   
    file_name = "NielsenImpression_"+zone_dict[zone_choice]+"_"+bcastWeek_dict[bcastWeek_choice]
    ##get the list of files matching the user slected criteria
    dataFile_list = fnmatch.filter(os.listdir('.'), file_name+'*.txt')
    
    
    ## create a new order id
    orderID = (len(tvOrderForecast_list) + 1)
    
    ## append the TVAdOrder object into tvOrderForecast_list
    ##tvadOrder_repr = repr(TVAdOrder(orderID,network_dict[network_choice],zone_dict[zone_choice], bcastWeek_dict[bcastWeek_choice], int(audience_choice),daypart_dict[daypart_choice],dataFile_list))
    
    ##tvOrderForecast_list.append(eval(tvadOrder_repr))
    before_length = len (tvOrderForecast_list) 
    tvOrderForecast_list.append(TVAdOrder(orderID,network_dict[network_choice],zone_dict[zone_choice], bcastWeek_dict[bcastWeek_choice], int(audience_choice),daypart_dict[daypart_choice],dataFile_list))    
    after_length = len (tvOrderForecast_list) 
    
    assert(after_length == (before_length + 1) ), "TvAdorder object creation failed"   
    
    ## Impression forecast is zero then diplay mesage as 'lack of data to forecast"
    if tvOrderForecast_list[orderID - 1].getImpressions() == 0 :
        print("\n\n CANNOT FORECAST DUE TO LACK OF DATA!!!")
    else :
        print("\n\n\n","{:<100s}".format("     Estimated count of viewers of your TV ad "),":" , tvOrderForecast_list[orderID - 1].getImpressions())
        print("\n","{:<100s}".format("     Estimated Price of your one TV ad spot you are targeting "),":", tvOrderForecast_list[orderID - 1].getSpotPrice())
    
    continue_function()
    
    return 0
    
    
    

def networkRecommend():
    
    #### Values TV spot recommendtaion page    
    
    currentChoice_dict=dict()     
    currentChoice_dict["Page"] = "--------------------VALUED TV SPOT RECOMMENDATION------------------------"
    
    ## Clear screen    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\n\n                                      ",currentChoice_dict["Page"],"\n\n")
     
    print("select one of the foll0wing ")
    recommendationOptions_choice = validChoice(recommendationOptions_dict,"RECOMMENDATION Page Option",currentChoice_dict)
    
    
    ## if the option is to list previous queries recomemndations then dispaly previous requests
    if recommendationOptions_choice == "2" :
       if len(recommendation_list) == 0 :
           print("\n\nNO SAVED RECOMMENDATIONS!!!")
           
           continue_function()
           return 0
           
       else :
           print("\n\n")
           print("{:<20s}".format("RecommendationID"),"{:<12s}".format("Zone"),"{:<28s}".format("TargetAudience"),"{:<15s}".format("BroadcastWeek"))
           print("------------------------------------------------------------------")
           for recommendation in recommendation_list :
               print("{:<20s}".format(str(recommendation[0])),"{:<12s}".format(recommendation[1]),"{:<28s}".format(str(recommendation[2])),"{:<15s}".format(str(recommendation[3])))
           
           
           ### Option to select previous recommendtaion 
           while True:
               print("\nEnter RecommendationID to select one of above Recommendation ")
               try:
                   recommendationID_choice = int(str(input()).strip(' '))
                   if recommendationID_choice not in range(1,(len(recommendation_list)+1)): raise ValueError
               except ValueError:
                   print("Inavlid RecommendationID choice!! TRY AGAIN!!")
                   continue
               break
           
           ## based on selected recommednation id diplay the data accordingly
           os.system('cls' if os.name == 'nt' else 'clear')
           print("\n\n\n                                      ",currentChoice_dict["Page"],"\n\n")
           print("\nVALUE SPOT RECOMMENDATION IN THE ORDER OF VALUE FOR\n")
           print("{:<20s}".format("RecommendationID"),"{:<12s}".format("Zone"),"{:<28s}".format("TargetAudience"),"{:<15s}".format("BroadcastWeek"))
           print("------------------------------------------------------------------")
           print("{:<20s}".format(str(recommendation_list[recommendationID_choice - 1][0])),"{:<12s}".format(recommendation_list[recommendationID_choice - 1][1]),"{:<28s}".format(str(recommendation_list[recommendationID_choice - 1][2])),"{:<15s}".format(str(recommendation_list[recommendationID_choice - 1][3])))
           print("\nIS     \n")
           print("{:<12s}".format("Network"),"{:<15s}".format("Daypart"),"|","{:<22s}".format("Viewers Estimate"),"{:<25s}".format("SpotPrice Estimate"))
           print("------------------------------------------------------------------------")
           
           record_ind = 0
           for tvAdOrder in recommendation_list[recommendationID_choice - 1][4]:
               
               if tvAdOrder.getImpressions() > 0 :
                   record_ind = 1
                   print("{:<12s}".format(tvAdOrder.getNetwork()),"{:<15s}".format(tvAdOrder.getDaypartName()),"|","{:<22s}".format(str(tvAdOrder.getImpressions())),"{:<25s}".format(str(tvAdOrder.getSpotPrice())))
                   ##print(tvAdOrder.getNetwork(),"        ",tvAdOrder.getDaypartName(),"     ", tvAdOrder.getImpressions(), "      ",tvAdOrder.getSpotPrice() )
           
           if record_ind == 0 : print ("NO RECOMMENDATIONS AVAILABLE DUE TO LACK OF DATA!!!")         
           
           continue_function()
           return 0
 
          
               
    #### if the user has selected to get new reommednations then do the following
    
    print("\nSelect zone of target Audience")
          
    zone_choice = validChoice(zone_dict,"Zone",currentChoice_dict)
    
    
    print("\nSelect Target Audience")
    
    audience_choice = validChoice(audience_dict,"Audience",currentChoice_dict)
    
   
    print("\nSelect Broadcast Week of year 2018")
    
    bcastWeek_choice = validChoice(bcastWeek_dict,"Broadcast Week",currentChoice_dict)
    

    ##### Narrow down the files from which the relevant data is filetred baed on user entered spot details
    ##### File name format is    NielsenImpression_{zone}_{broadcastweek}_{year}.txt
    file_name = "NielsenImpression_"+zone_dict[zone_choice]+"_"+bcastWeek_dict[bcastWeek_choice]
    
    ##get the list of files matching the user slected criteria
    dataFile_list = fnmatch.filter(os.listdir('.'), file_name+'*.txt')
    
    ## empty list to hold all tv order for the search criteria  
    tvAdOrder_list = list()
    
    ## create TV order list for all possible networks and dayparts
    for key, daypart in daypart_dict.items() :
        
        for key, network in network_dict.items() :
            
                orderId = len(tvAdOrder_list) + 1
            
                tvAdOrder_list.append(TVAdOrder(orderId,network,zone_dict[zone_choice], bcastWeek_dict[bcastWeek_choice], int(audience_choice),daypart,dataFile_list))

    ## Create empty dictionary to hold impression and spotrates of all possibel TV orders created above
    tvAdOrderImpression_dict=dict()
    tvAdOrderSpotPrice_dict=dict()
    
    ## append al impression values, spotartes and corresponding orderids to above created dictionaries
    for tvAdOrder in tvAdOrder_list:
        
        tvAdOrderImpression_dict[tvAdOrder.getOrderId()] = tvAdOrder.getImpressions()
        tvAdOrderSpotPrice_dict[tvAdOrder.getOrderId()] = tvAdOrder.getSpotPrice()
        
    ## sort the impression values from highest to lowest along with their orderids
    tvAdOrderImpression_sort_tuple = sorted(tvAdOrderImpression_dict.items(), key=lambda x: x[1], reverse = True) 

    ## sort the spotprice values from lowest to highest along with their orderids
    tvAdOrderSpotPrice_sort_tuple = sorted(tvAdOrderSpotPrice_dict.items(), key=lambda x: x[1]) 
    ##print(tvAdOrderSpotPrice_sort_tuple)
    
    
    ## get the combined rank of all orders created based on highest impression and lowest spotprice
    recommendation_order_dict=dict()
    for order1 in tvAdOrderImpression_sort_tuple:
        
        for order2 in tvAdOrderSpotPrice_sort_tuple:
            if order1[0] == order2[0] :
                recommendation_order_dict[order1[0]] = (tvAdOrderImpression_sort_tuple.index(order1) + tvAdOrderSpotPrice_sort_tuple.index(order2))
                break
            
    ##  sort the combined rank of highest imrpessiona dn lowest spotprices from lowest to highest
    ##  meaning lowest rank has better value with high impression and low spotprice
    recommendation_sort_tuple = sorted(recommendation_order_dict.items(), key=lambda x: x[1])
    ##print(recommendation_sort_tuple)
    

    ## append the recommendation into a list of lists
    ## where in each list has 5 elements
    ## 1. recommenddation id generated 
    ## 2. Zone slected by user
    ## 3. target audience selected by user
    ## 4. bcastweek selected by user
    ## 5. List of all spots in the order of value meaninng first spot in the list has highest impression with low spotprice
    recomemndation_ID = (len(recommendation_list) + 1)
    recommendation_list.append([recomemndation_ID,zone_dict[zone_choice],audience_dict[audience_choice],bcastWeek_dict[bcastWeek_choice],[]])
    
    
    ## Add all the recommended orders in the 4 index list       
    for order in  recommendation_sort_tuple:
        for tvAdOrder in tvAdOrder_list:
            if order[0] == tvAdOrder.getOrderId() :
                before_length = len (recommendation_list[recomemndation_ID - 1][4])
                recommendation_list[recomemndation_ID - 1][4].append(tvAdOrder)
                after_length = len (recommendation_list[recomemndation_ID - 1][4])
                assert(after_length == (before_length + 1)),"Failed saving recommendation!!!"
    ## diplay recommendation accordingly
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\n\n                                      ",currentChoice_dict["Page"],"\n\n")
    print("\nVALUE SPOT RECOMMENDATION IN THE ORDER OF VALUE FOR\n")
    print("{:<20s}".format("RecommendationID"),"{:<12s}".format("Zone"),"{:<28s}".format("TargetAudience"),"{:<15s}".format("BroadcastWeek"))
    print("------------------------------------------------------------------")
    print("{:<20s}".format(str(recommendation_list[recomemndation_ID - 1][0])),"{:<12s}".format(recommendation_list[recomemndation_ID - 1][1]),"{:<28s}".format(str(recommendation_list[recomemndation_ID - 1][2])),"{:<15s}".format(str(recommendation_list[recomemndation_ID - 1][3])))
    print("\nIS     \n")
  
    print("{:<12s}".format("Network"),"{:<15s}".format("Daypart"),"|","{:<22s}".format("Viewers Estimate"),"{:<25s}".format("SpotPrice Estimate"))
    print("------------------------------------------------------------------------")
    
    record_ind = 0       
    for tvAdOrder in recommendation_list[recomemndation_ID - 1][4]:
        if tvAdOrder.getImpressions() > 0 :
            record_ind = 1
            print("{:<12s}".format(tvAdOrder.getNetwork()),"{:<15s}".format(tvAdOrder.getDaypartName()),"|","{:<22s}".format(str(tvAdOrder.getImpressions())),"{:<25s}".format(str(tvAdOrder.getSpotPrice())))
    
    if record_ind == 0 : print ("NO RECOMMENDATIONS AVAILABLE DUE TO LACK OF DATA!!!")
    
    continue_function()
    return 0            
    




def main():
    
  """
     main program
     
  """
  ## acll fucntion with initial setup
  initail_setup()

  while True: 
      ##Clear screen
      os.system('cls' if os.name == 'nt' else 'clear')
      
      Page = "--------------------TV ADVERTISING RECOMMENDATION TOOL------------------------"
      print("\n\n\n                                      ",Page,"\n\n")
      
      print("\n\n\n\
        Please select the purpose of using this tool:\n\
            1. Forecast viweers count for a given TV ad Spot and its price\n\
            2. Network Recommendations for reaching specific Audience group \n" )
      
      while True:
          print("\nEnter Number listed above against your choice :")

          try:
              purpose_choice = int(str(input()).strip(' '))
          
              if purpose_choice not in [1,2] : raise ValueError
              
          except ValueError:
              print("Invalid Choice!! TRY AGAIN!!")
              continue
          
          break
      
  
      if purpose_choice == 1 :
          forecastAudience()
      
      else :
          networkRecommend()
      
  exit()


####### CAll MAIN FUNCTION ########################  
main()


        
        
                
        