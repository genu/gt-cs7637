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
from itertools import permutations



def pythonize(problem):
    """Returns a pythonic version of a problem object"""
    
    def parse_attr(name, value):
        lists = ['above', 'left-of', 'inside', 'overlaps']
        bools = ['vertical-flip', 'horizontal-flip']
        sizes = ['size']
        nums = ['angle']
        shapes = ['shape']
        fills = ['fill']
        
        
        if name in lists:
            value = value.split(',')
        elif name in bools:
            if value == 'yes':
                value = True
            else:
                value = False
        elif name in sizes:
            if value == 'small':
                value = 1
            elif value == 'medium':
                value = 2
            elif value == 'large':
                value = 3
            else:
                value = 0
        elif name in nums:
            value = float(value)
        elif name in shapes or name in fills:
            pass
        else:
            print "unknown: %s-%s" % (name, value)
        return value
        
    ret = {}
    figures = {}
    
    for fig in problem.getFigures().values():
        objs = {}
        for obj in fig.getObjects():
            attrs = {}
            for attr in obj.getAttributes():
                attrs[attr.getName()] = parse_attr(attr.getName(), attr.getValue())
            objs[obj.getName()] = attrs
        figures[fig.getName()] = objs
        
    ret['type'] = problem.getProblemType()
    ret['name'] = problem.getName()
    ret['figures'] = figures
    return ret
    
    
def permute_fig_shapes(fig):
    """Returns a list of possible permutations (names) of shapes in a fig."""
    names = fig.keys()
    shapes = fig.values()
    ret = []
    
    for p in permutations(range(len(fig))):
        tfig = {}
        for i in range(len(p)):
            tfig[names[i]] = shapes[p[i]]
        ret += [tfig]
    
    return ret
        


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
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
        if not "05" in problem.name: return "-1"
        oproblem = problem
        problem = pythonize(problem)
        pprint(problem)
        ret = '6'
        
        figures = problem['figures']
        
        if problem['type'] == '2x1':
            print "******Identifying possile transformations from A to B...******"
            target_transforms = self.build_permuted_transforms(figures['A'], figures['B'])
            
            pprint(target_transforms)

            choice_transforms = {}
            diffs = {}
            for i in range(1, 7):
                i = str(i)
                print "*******Identifying possible transfomrations from C to %s******" % i
                choice_transforms[i] = self.build_permuted_transforms(figures['C'], figures[i])
                
            best_score = float('inf')
            best_weight = float('-inf')

            print "******Finding best combo...*******"
            for target_trans in target_transforms:
                for i in choice_transforms:
                    for choice_trans in choice_transforms[i]:
                        score = self.compare_transforms(target_trans, choice_trans)
                        if score < best_score:
                            print('****Better combo found: C->%s, score %d****' % (i, score))
                            print('A->B')
                            pprint(target_trans)
                            print('C->%s' % i)
                            pprint(choice_trans)
                            best_score = score
                            best_weight = self.weight_transform_graph(target_trans)
                            ret = i
                        elif score == best_score:
                            weight = self.weight_transform_graph(target_trans)
                            if weight > best_weight:
                                print('****Better weighted combo found: C->%s, weight %d****' % (i, score))
                                print('A->B')
                                pprint(target_trans)
                                print('C->%s' % i)
                                pprint(choice_trans)
                                best_weight = self.weight_transform_graph(target_trans)
                                ret = i
                            
            actual_answer = oproblem.checkAnswer(ret)
            if actual_answer == ret:
                print('CORRECT: chose %s' % ret)
            else:
                print('INCORRECT: chose %s, wanted %s' % (ret, actual_answer))
            
        # x = raw_input('Press enter to continue, q to quit... ')
        #         if x.lower() == 'q':
        #             exit()

        return ret
    
    def compare_transforms(self, t1, t2):
        diffs = 0
        for t in t1:
            if not t in t2:
                diffs += 1
                continue
            if t1[t] != t2[t]:
                diffs += 1
        for t in t2:
            if not t in t1:
                diffs += 1
        return diffs
    
    
    def weight_transform_graph(self, graph):
        score = 0 
        for shape in graph:
            if len(shape) == 0:
                # unchanged
                continue
            for trans in graph[shape]:
                if 'above' in trans or 'left-of' in trans or 'inside' in trans or 'overlaps' in trans:
                    score -= 1
                if 'flipped' in trans:
                    score -= 1
                elif 'filled' in trans:
                    score -= 1
                elif 'rotated' in trans:
                    score -= 2
                elif 'expanded' in trans or 'shrunk' in trans:
                    score -= 3
                elif 'deleted' in trans:
                    score -= 4
                elif 'reshaped' in trans:
                    score -= 5
        return score
        
    
    
    
    
    def identify_trans(self, shape1, shape2):
        positionals = ['above', 'left-of', 'inside', 'overlaps']
        
        trans = []
        if shape2.get('size', 0) > shape1.get('size', 0):
            trans += ['expanded']
        if shape2.get('size', 0) < shape1.get('size', 0):
            trans += ['shrunk']
        if shape2.get('fill', False) != shape1.get('fill', False):
            trans += ['filled %s' % shape2.get('fill', False)]
        if shape2.get('shape', 'square') != shape1.get('shape', 'square'):
            trans += ['reshaped from %s to %s' % (shape1.get('shape', 'square'), shape2.get('shape', 'square'))]
        if shape2.get('angle', 0) != shape1.get('angle', 0):
            angle_diff = (shape2.get('angle', 0) - shape1.get('angle', 0)) % 360
            trans += ['rotated %f' % angle_diff]
        # if shape2.get('horizontal-flip', False) != shape1.get('horizontal-flip', False):
        #     trans += ['horizontal-flipped from %s to %s' % (shape1.get('horizontal-flip', False), shape2.get('horizontal-flip', False))]
        # if shape2.get('vertical-flip', False) != shape1.get('vertical-flip', False):
        #     trans += ['vertical-flipped from %s to %s' % (shape1.get('vertical-flip', False), shape2.get('vertical-flip', False))]
        for positional in positionals:
            if shape2.get(positional, None) != shape1.get(positional, None):
                trans += [positional + str(shape2.get(positional, ''))]
        
        return trans
    
    
    def build_permuted_transforms(self, f1, f2):
        """Considers all possible transformations between two figures (unless there are a large number of figures)"""
        
        if len(f2) < 7:
            f2_permutes = permute_fig_shapes(f2)
        else:
            print "Too many shapes - not permuting"
            f2_permutes = [f2]
        
        ret = []
        for f in f2_permutes:
            ret += [self.build_transform(f1, f)]
        
        return ret
    
    def build_transform(self, f1, f2):
        """Builds a transformation graph between two figures"""
        
        graph = {}
        
        for shape in f1:
            graph[shape] = []
            if not shape in f2:
                graph[shape] += ['deleted']
                continue
            graph[shape] += self.identify_trans(f1[shape], f2[shape])
            
        
        return graph
    
        
