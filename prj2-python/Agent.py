# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.


from pprint import pprint
# from itertools import permutations


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        # knowledge base - lets our Agent acquire and learn info from each problem
        self.kb = {}
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem
    def Solve(self, problem):
        ret = '6'
        
        oproblem = problem
        problem = pythonize(problem)
        figures = problem['figures']
        
        # Debug code for jumping to specific problems
        # if not '2x2' in problem['name']:
        #     return '8'
        
        #pprint(problem)
        print problem['name']
        self.scan_attrs(problem)
        
        # 2x1
        if problem['type'] == '2x1':
            old_b = figures['B']
            # remap B's parts to A's based on similarity
            figures['B'] = self.get_renamed_figure(figures['A'], figures['B'])
            target_rels = self.find_relationships(figures['A'], figures['B'])
            print('A')
            pprint(figures['A'])
            if old_b != figures['B']:
                print('ORIGINAL B')
                pprint(old_b)
                
            print('REMAPPED B')
            pprint(figures['B'])
            print('A->B')
            pprint(target_rels)
            
            scores = {}
            
            for i in range(1, 7):
                i = str(i)
                old_fig = figures[i]
                # remap choice's parts to C's based on similarity
                figures[i] = self.get_renamed_figure(figures['C'], figures[i])
                choice_rels = self.find_relationships(figures['C'], figures[i])
                print('C->%s' % i)
                pprint(choice_rels)
                scores[i] = self.score_relationships(target_rels, choice_rels)
                print('Score: %f' % scores[i])
            
            scores = sorted(scores.items(), key=lambda score:score[1], reverse=True)
            pprint(scores)
            print 'choosing %s with score of %f' % (scores[0][0], scores[0][1])
            ret = scores[0][0]
        
        
        # 2x2
        if problem['type'] == '2x2':
            # remap B and C's parts to A's based on similarity
            figures['B'] = self.get_renamed_figure(figures['A'], figures['B'])
            figures['C'] = self.get_renamed_figure(figures['A'], figures['C'])
            
            x_target_rels = self.find_relationships(figures['A'], figures['B'])
            y_target_rels = self.find_relationships(figures['A'], figures['C'])
            
            print('A->B')
            pprint(x_target_rels)
            print('A->C')
            pprint(y_target_rels)
            
            scores = {}
            
            for i in range(1, 7):
                i = str(i)
                # remap choice's parts to C's based on similarity
                x_fig = self.get_renamed_figure(figures['C'], figures[i])
                x_choice_rels = self.find_relationships(figures['C'], x_fig)
                print('C->%s' % i)
                pprint(x_choice_rels)
                x_score = self.score_relationships(x_target_rels, x_choice_rels)
                print('Score: %f' % x_score)

                y_fig = self.get_renamed_figure(figures['B'], figures[i])
                y_choice_rels = self.find_relationships(figures['B'], y_fig)
                print('B->%s' % i)
                pprint(y_choice_rels)
                y_score = self.score_relationships(y_target_rels, y_choice_rels)
                print('Score: %f' % y_score)
                
                scores[i] = x_score + y_score
                
            
            scores = sorted(scores.items(), key=lambda score:score[1], reverse=True)
            pprint(scores)
            print 'choosing %s with score of %f' % (scores[0][0], scores[0][1])
            ret = scores[0][0]
        
        # for fig in ['B', 'C']:
        #     problem['figures'][fig] = self.get_renamed_figure(problem['figures']['A'], problem['figures'][fig])
        #     rels = self.find_relationships(problem['figures']['A'], problem['figures'][fig])
        #     print('A->%s' % fig)
        #     pprint(rels)
        
        return ret

    
    
    def scan_attrs(self, prob):
        """Looks at the current problem's attributes, stores them in the KB"""
        
        # Keep track of the names of objects in the current problem
        # (useful to determine if attributes are referring to other objects)
        object_names = []
        for fig in prob['figures'].values():
            for object_name in fig.keys():
                if not object_name in object_names:
                    object_names.append(object_name)
        
        if not 'attributes' in self.kb:
            self.kb['attributes'] = {}
        
        attrs = self.kb['attributes']
        
        # process the attributes in the current problem
        for fig in prob['figures'].values():
            for obj in fig.values():
                for attr, subvalues in obj.items():
                    if not attr in attrs:
                        attrs[attr] = {'values': [],
                                       'relative': 'unknown',
                                       'multi': 'unknown',
                                       'count': 0}
                    data = attrs[attr]
                    
                    data['count'] += 1
                    
                    if data['multi'] == 'unknown':
                        if len(subvalues) > 1:
                            data['multi'] = 'yes'
                        else:
                            data['multi'] = 'no'
                    else:
                        if len(subvalues) > 1 and data['multi'] == 'no':
                            data['multi'] = 'sometimes'
                        elif len(subvalues) == 1 and data['multi'] == 'yes':
                            data['multi'] = 'sometimes'
                    
                    # process each subvalue
                    values = data['values']
                    for subvalue in subvalues:
                        # check to see if this attr refers to other objects
                        relative = False
                        if subvalue in object_names:
                            relative = True
                            if data['relative'] == 'unknown':
                                data['relative'] = 'yes'
                            elif data['relative' ] == 'no':
                                data['relative'] = 'sometimes'
                        else:
                            if data['relative'] == 'unknown':
                                data['relative'] = 'no'
                            elif data['relative'] == 'yes':
                                data['relative'] = 'sometimes'
                        
                        # add this to the seen values if it isn't already
                        # in there and it isn't a relative value
                        if not relative and not subvalue in values:
                            values.append(subvalue)
        
        # update the kb's attribute priorities based upon frequency of encounters
    
        sorted_attrs = sorted(attrs.items(), key=lambda attr: attr[1]['count'], reverse=True)
        priorities = self.kb['attribute_priorities'] = []
        for attr in sorted_attrs:
            priorities.append(attr[0])
    
    
    def get_renamed_figure(self, fig1, fig2):
        """Renames objects in fig2 based on analogies found from fig1 to fig2"""
        analogies = self.find_analogies(fig1, fig2)
        
        for obj2 in fig2:
            if not obj2 in analogies.values():
                analogies['_%s' % obj2] = obj2 # add an underscore to prevent name conflicts
        
        print "Analogies:"
        pprint(analogies)
        
        ret = {}
        
        for obj1, obj2 in analogies.items():
            if obj2 in fig2:
                ret[obj1] = fig2[obj2]
        
        return ret
        
        
    
    
    def find_analogies(self, fig1, fig2):
        """Finds analogies from fig1 to fig2. Recommend making fig1 the simpler fig."""
        
        if len(fig1) == 0 or len(fig2) == 0:
            return {}
        
        analogies = {} # map from fig1_name: (fig2_name, score)
        
        for obj1, attrs1 in fig1.items():
            matches = {}
            
            for obj2, attrs2 in fig2.items():
                score = 0
                max_score = 0
                
                for attr, value1 in attrs1.items():
                    cur_points = 1
                    if not attr in attrs2:
                        # doesn't exist in other object, skip it
                        continue
                    
                    if attr in self.kb['attribute_priorities']:
                        priority_rank = self.kb['attribute_priorities'].index(attr)
                        if priority_rank < 5:
                            cur_points += 2.0/(priority_rank + 1)


                    value2 = attrs2[attr]
                    if self.kb['attributes'][attr]['relative'] != 'no':
                        cur_points += 1
                        # this is a relative attribute, so names will be different
                        # just look at the length of the value
                        if len(value1) == len(value2):
                            score += cur_points
                    elif value1 == value2:
                        # exact match, increase score
                        score += cur_points
                    
                    max_score += cur_points
                        
                matches[obj2] = score / float(max_score)
            
            analogies[obj1] = sorted(matches.items(), key=lambda match: match[1], reverse=True)
        
        ret = {} # map from obj1: obj2
        
        while len(analogies) > 0:
            pprint(analogies)
            sorted_analogies = sorted(analogies.items(), key=lambda analogy: analogy[1][0][1], reverse=True)
            pprint(sorted_analogies)
            
            obj1 = sorted_analogies[0][0]
            obj2 = sorted_analogies[0][1][0][0]
            
            ret[obj1] = obj2
            
            # remove obj2 from any other analogies findings
            for i in analogies.keys():
                for j in range(len(analogies[i]) - 1, -1, -1):
                    if analogies[i][j][0] == obj2:
                        del analogies[i][j]
                if len(analogies[i]) == 0:
                    del analogies[i]
            
        
        return ret
        
                
    def find_relationships(self, fig1, fig2):
        """Finds the relationships from fig1 to fig2."""
        
        rels = []
        
        # relationship based on # of objects
        if len(fig1) == len(fig2):
            rels.append({'obj': 'all', 'attr': 'count', 'type': 'match'})
        else:
            rels.append({'obj': 'all', 'attr': 'count', 'type': 'mismatch'})
        
        for obj, attrs in fig1.items():
            if not obj in fig2:
                # object has been removed in fig2
                rels.append({'obj': obj, 'attr': 'all', 'type': 'removed'})
                continue
        
        for obj in fig2:
            if not obj in fig1:
                # object is only present in fig2
                rels.append({'obj': obj, 'attr': 'all', 'type': 'added'})
                continue
            
            for attr in fig2[obj]:
                rel = {'obj': obj, 'attr': attr}
                
                if attr in fig1[obj] and fig1[obj][attr] == fig2[obj][attr]:
                    rel['type'] = 'match'
                else:
                    partial_match = False
                    for subvalue in fig2[obj][attr]:
                        if attr in fig1[obj] and subvalue in fig1[obj][attr]:
                            partial_match = True
                    
                    if partial_match:
                        rel['type'] = 'partial'
                    else:
                        rel['type'] = 'mismatch'
                        rel['old_values'] = ','.join(fig1[obj].get(attr, ['missing']))
                        rel['new_values'] = ','.join(fig2[obj][attr])
                        if rel['new_values'].isdigit() and rel['old_values'].isdigit():
                            rel['diff'] = float(rel['new_values']) - float(rel['old_values'])
                            del rel['old_values']
                            del rel['new_values']
                
                rels.append(rel)
        
        return rels
    

    def score_relationships(self, rels1, rels2):
        
        # keep track of score and max score to give a weighted result
        
        # one point if they have the same number of entries
        if len(rels1) == len(rels2):
            score = 1
        else:
            score = 0
        max_score = 1
        
        # look for each of the relationships from rels1 in rels2
        for rel in rels1:
            # assign the current points based upon the type of match
            if rel['type'] == 'match':
                cur_points = 1
            elif rel['type'] == 'mismatch':
                cur_points = 0.5
            else:
                cur_points = 0.25
            
            # give a bonus for higher "priority" attributes
            if rel['attr'] in self.kb['attribute_priorities']:
                priority_rank = self.kb['attribute_priorities'].index(rel['attr'])
                if priority_rank < 5:
                    cur_points += 1.0/(priority_rank + 1)
            
            max_score += cur_points
            
            if rel in rels2:
                score += cur_points
                
        
        # normalize score
        return score / float(max_score)
    


def pythonize(problem):
    """Returns a pythonic version of a problem object"""
    
    ret = {}
    ret['type'] = problem.getProblemType()
    ret['name'] = problem.getName()
    ret['figures'] = figures = {}
    
    for fig in problem.getFigures().values():
        figures[fig.getName()] = objs = {}
        for obj in fig.getObjects():
            objs[obj.getName()] = attrs = {}
            for attr in obj.getAttributes():
                value = attr.getValue()
                values = [value]
                if ',' in value:
                    values = value.split(',')
                attrs[attr.getName()] = values
    
    return ret