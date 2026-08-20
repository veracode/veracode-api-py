# internal helper methods
class Utilities():

   def case_insensitive_list_compare(self,input_list:list, target_list:list):
      input_set = self.lowercase_set_from_list(input_list)
      target_set = self.lowercase_set_from_list(target_list)
      return target_set.issuperset(input_set)

   def lowercase_set_from_list(self,thelist:list):
      return set([x.lower() for x in thelist])