import pandas as pd
import math

class MAPSKB():
    """
        MAPS-KB: A Million-scale Probabilistic Simile Knowledge Base
        includes 4.3 million simile triplets in the form of (topic, property, vehicle) 
        along with two probabilistic metrics, plausibility and typicality, to model them.
    """

    def __init__(self, KB_path):
        """
        :param KB_path: file path to the MAPS-KB(.csv)
        """
        self.KB = pd.read_csv(KB_path)

    def lookup(self, topic= None, vehicle = None , property= None):
        """
        :param topic: topic of the simile (e.g. 'He' in the simile 'He is as tall as a tree'.)
        :param vehicle: vehicle of the simile (e.g. 'a tree' in the simile 'He is as tall as a tree'.)
        :param property: property of the simile (e.g. 'tall' in the simile 'He is as tall as a tree'.)
        :return: a pandas dataframe containing the simile triplets and their probabilistic metrics that match the query
        """
        query_topic = True
        query_vehicle = True
        query_property = True

        if topic != None:
            query_topic = (self.KB['new_topic'] == topic)
        if vehicle != None:
            query_vehicle = (self.KB['new_vehicle'] == vehicle)
        if property != None:
            query_property = (self.KB['property'] == property)
        
        return self.KB.loc[query_topic & query_vehicle & query_property]


    def SI(self, vehicle, topk_triplets = 500, topk_return = 5):
        """
        Simile Interpretation task: given a vehicle, find the most plausible properties of the vehicle.
        :param vehicle: vehicle of the simile (e.g. 'a tree' in the simile 'He is as tall as a tree'.)
        :param topk_triplets: number of triplets to consider
        :param topk_return: number of properties to return
        :return: a list of properties
        """
        fill_list = self.KB.loc[(self.KB['new_vehicle'] == vehicle)]
        _ = fill_list.sort_values(by="count" , ascending=False)

        property = list(_['property'])
        count = list(_['count'])
        plausibility = list(_['plausibility'])
        typicality = list(_['typicality_p_to_tvpair'])

        final_dict = {}
        for ii in range(min(topk_triplets,len(plausibility))):
            if property[ii] not in final_dict:
                final_dict[property[ii]] = 0
            final_dict[property[ii]] += typicality[ii]*plausibility[ii]*count[ii]
        
        p_list = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)
        p_list = [i[0] for i in p_list]

        return p_list[:topk_return]

    def SG(self, property, topk_triplets = 10, topk_return = 5, alpha = 2):
        """
        Simile Generation task: given a property, find the most plausible vehicles of the property.
        :param property: property of the simile (e.g. 'tall' in the simile 'He is as tall as a tree'.)
        :param topk_triplets: number of triplets to consider
        :param topk_return: number of vehicles to return
        :param alpha: the parameter to encourage longer vehicles which tend to be more expressive.
        :return: a list of vehicles
        """
        fill_list = self.KB.loc[self.KB.property == property]
        if len(fill_list) == 0:
            return []
        _ = fill_list.sort_values(by="count" , ascending=False)

        new_vehicle = list(_['new_vehicle'])
        count = list(_['count'])
        plausibility = list(_['plausibility'])
        typicality = list(_['typicality_tvpair_to_p'])

        final_dict = {}
        for ii in range(min(topk_triplets,len(plausibility))):
            if new_vehicle[ii] not in final_dict:
                final_dict[new_vehicle[ii]] = 0
            # 引入比例
            alpha = 2
            final_dict[new_vehicle[ii]] += typicality[ii]*plausibility[ii]*count[ii]*math.exp(len(alpha * new_vehicle[ii].split(' ')))
        syn_veh_list = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)
        syn_veh_list = [i[0] for i in syn_veh_list]
        return syn_veh_list[:topk_return]


