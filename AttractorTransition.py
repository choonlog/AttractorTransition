'''

'''
from sympy.logic.boolalg import to_dnf
import cana
from cana.datasets.bio import THALIANA
import re
import itertools
import random
import collections



# hyper-parameters
one_plus_product_net_max_num = 100



def modeltext_transform(modeltext):


    # Replace the logics with symbols
    modeltext = re.sub(r"\band\b", "&", modeltext)
    modeltext = re.sub(r"\bor\b", "|", modeltext)
    modeltext = re.sub(r"\bnot\b", "~", modeltext)

    # strip modeltext
    modeltext = modeltext.strip()

    # split the modeltext by line
    modeltext_lines = modeltext.splitlines()

    modeltext_extra = ""
    for modeltext_line in modeltext_lines:
        node_list = re.findall(r'\w+', modeltext_line)
        modeltext_line_extra = modeltext_line

        for node in node_list:
            modeltext_line_extra = re.sub(r"\b" + node + r"\b", node + "_", modeltext_line_extra)

        modeltext_extra += modeltext_line_extra + "\n"
    return modeltext_extra


def DFS(graph, start_vertex, onlyOnePlusProduct):
    visited = set()
    traversal = []
    stack = [start_vertex]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            traversal.append(vertex)
            if vertex in onlyOnePlusProduct:
                try:
                    stack.extend(reversed(graph[vertex]))   # add vertex in the same order as visited
                except:
                    pass
    return traversal



def one_plus_prodcut(allPlusProduct):
    allPlusProduct = allPlusProduct.strip()
    allPlusProductLine = allPlusProduct.splitlines()

    onlyOnePlusProduct = []
    multiPlusProducts = []
    selfFeedbackNode = []
    graph = {}
    multiPlusProductDic = {}
    allPlusProductDic = {}
    for line in allPlusProductLine:
        lineSplit = line.split("=")
        outputNode = lineSplit[0].strip()
        inputNode = lineSplit[1].strip()

        allPlusProductDic[outputNode] = inputNode

        inputNodeSplit = inputNode.split(" | ")
        if len(inputNodeSplit) == 1:
            if not outputNode in inputNode:
                # Only one plus product
                onlyOnePlusProduct.append(outputNode)
            else:
                # multi plus products
                selfFeedbackNode.append(outputNode)
        else:
            multiPlusProducts.append(outputNode)
            multiPlusProductDic[outputNode] = inputNode

        # Extract nodes from each logic expression and create one list
        inputNodeList = re.findall(r'\w+', inputNode)

        # Remove duplicates in list
        inputNodeList = [x for i, x in enumerate(inputNodeList) if i == inputNodeList.index(x)]

        # Set the input of DFS function
        graph[outputNode] = inputNodeList

    multiPlusProductDicRaw = multiPlusProductDic.copy()

    for multiPlusProduct in multiPlusProducts:
        for multiPlusProductInput in graph[multiPlusProduct]:
            # Call DFS function
            if multiPlusProduct in DFS(graph, multiPlusProductInput, onlyOnePlusProduct):
                multiPlusProductDic[multiPlusProduct] = re.sub(r"\b" + multiPlusProductInput + r"\b", '1', multiPlusProductDic[multiPlusProduct])
            else:
                multiPlusProductDic[multiPlusProduct] = re.sub(r"\b" + multiPlusProductInput + r"\b", '0', multiPlusProductDic[multiPlusProduct])

        termList = multiPlusProductDicRaw[multiPlusProduct].split(" | ")
        scoreList = multiPlusProductDic[multiPlusProduct].split(" | ")
        scoreDic = {}
        for term, score in zip(termList, scoreList):
            score = score.replace("&", "+")
            score = eval(score)
            scoreDic[term] = score

        # Find minimum value in dictionary
        result = min(scoreDic.items(), key=lambda k: k[1])
        allPlusProductDic[multiPlusProduct] = list(result)[0]

    formatTransform = ""
    formatFVS = ""
    for node in allPlusProductDic:
        BooleanExpression = node + " = " + allPlusProductDic[node]
        formatTransform += BooleanExpression + "\n"

        BooleanExpressionList = re.findall(r'\w+', BooleanExpression)
        BooleanExpressionListOutput = BooleanExpressionList[0]
        BooleanExpressionListInput = BooleanExpressionList[1:]

        # Remove duplicates in list
        BooleanExpressionListInput = [x for i, x in enumerate(BooleanExpressionListInput) if i == BooleanExpressionListInput.index(x)]

        for v in BooleanExpressionListInput:
            formatFVS += BooleanExpressionListOutput + ", " + v + "\n"

    return formatTransform, formatFVS



def remove_monostable_node(G_hat):

    # Split text lines
    modeltext_line = G_hat.splitlines()
    modeltext_extra = ""
    for line in modeltext_line:
        BooleanFunction = line.split("=")
        state_variable = BooleanFunction[0].strip()
        Boolean_expression = BooleanFunction[1].strip()

        if Boolean_expression.strip() == "":
            modeltext_extra += state_variable + " = " + state_variable + "\n"
        else:
            modeltext_extra += state_variable + " = " + Boolean_expression + "\n"

    return modeltext_extra.strip()



def mFVSs(modeltext):
    modeltext = modeltext.replace("=", "*=")
    net = cana.boolean_network.BooleanNetwork.from_string_boolean(modeltext)

    # Mapping nodes
    mappind_dic = {}
    for node in net.nodes:
        mappind_dic[node.id] = node.name

    # FVSs
    FVS_bruteforce = net.feedback_vertex_set_driver_nodes(graph='structural', method='bruteforce', max_search=10, keep_self_loops=True)  # brutuforce

    FVS_list_list = []
    for FVS in FVS_bruteforce:
        FVS_list = []
        for node in FVS:
            FVS_list.append(mappind_dic[node][:-1])
        FVS_list_list.append(FVS_list)

    return FVS_list_list



def canalizing(modeltext, canalizing_node_dic):

    # Strip whitespace
    modeltext = modeltext.strip()

    # Replace the logics with symbols
    modeltext = re.sub(r"\band\b", "&", modeltext)
    modeltext = re.sub(r"\bor\b", "|", modeltext)
    modeltext = re.sub(r"\bnot\b", "~", modeltext)

    # Split text lines
    modeltext_line = modeltext.splitlines()

    # Get all nodes
    all_node_list = []
    for line in modeltext_line:
        all_node_list += re.findall(r'\w+', line)

    # Deduplication
    all_node_list = [x for i, x in enumerate(all_node_list) if i == all_node_list.index(x)]

    # Create a all state vector dictionary with no values
    all_state_vector_dic = {}
    for node in all_node_list:
        all_state_vector_dic[node] = ""

    # Recursive process
    canalized_state_vector_dic = {}
    step_canalized_state_vector_list = []
    process = True
    while process:

        # Update canalizing node list
        if canalizing_node_dic:
            for node in canalizing_node_dic:
                all_state_vector_dic[node] = canalizing_node_dic[node]

            # Append canalized state vector list according to the step
            step_canalized_state_vector_list.append(canalizing_node_dic)

            # Merge two dictionaries
            canalized_state_vector_dic = dict(**canalized_state_vector_dic, **canalizing_node_dic)

            # Get canalizing node list
            canalizing_node_list = list(canalizing_node_dic.keys())

            # Split text lines
            modeltext_line = modeltext.splitlines()

            # Apply the canalization effect
            new_canalizing_node_dic = {}
            new_modeltext = ""
            for line in modeltext_line:
                str1 = line.split("=")
                state_variable = str1[0].strip()
                Boolean_expression = str1[1].strip()
                if not state_variable in canalizing_node_list:
                    for fixedNode in canalizing_node_dic:
                        Boolean_expression = re.sub(r"\b" + fixedNode + r"\b", str(canalizing_node_dic[fixedNode]).lower(), Boolean_expression)
                    simplifiedExpression = to_dnf(Boolean_expression)
                    if simplifiedExpression in [True, False]:
                        new_canalizing_node_dic[state_variable] = simplifiedExpression
                    else:
                        new_modeltext += state_variable + " = " + str(simplifiedExpression) + "\n"
            modeltext = new_modeltext
            canalizing_node_dic = new_canalizing_node_dic
        else:
            break

    # Remove whitespace
    modeltext = modeltext.strip()



    return modeltext



def replace_multiple(main_string, to_be_replaces, new_string):
    # Iterate over the strings to be replaced
    for elem in to_be_replaces:
        # Check if string is in the main string
        if elem in main_string:
            # Replace the string
            main_string = main_string.replace(elem, new_string)

    return main_string



def main(modeltext, initial_state, desired_attractor):

    # transform of modeltext
    modeltext = modeltext_transform(modeltext)

    # cycle check
    star_idx = [i for i, n in enumerate(desired_attractor) if n == '*']
    if len(star_idx) == 0:
        type = "point"
    else:
        type = "cycle"

    # if cycle, replace * with 1
    desired_attractor = desired_attractor.replace("*", "1")

    # strip modeltext
    modeltext = modeltext.strip()

    # split the modeltext by line
    modeltext_line = modeltext.splitlines()

    # convert the desired_attractor to dictionary logic type
    desired_attractor_dic = {}
    s = 0
    for line in modeltext_line:
        IODic = line.split("=")
        desired_attractor_dic[IODic[0].strip()] = str(bool(int(desired_attractor[s])))
        s = s + 1

    # set logic symbols
    and_logic = ["and", "&&"]
    or_logic = ["or", "||"]
    negation_logic = ["not"]

    # convert each logic expression to disjunctive normal form(DNF)
    format_transform_raw = ""
    format_transform_all_plus_product = ""
    cycle_node_list = []
    for i, line in enumerate(modeltext_line):

        # Convert given logic symbols to official symbols
        and_rep = replace_multiple(line, and_logic, "&")
        or_rep = replace_multiple(and_rep, or_logic, "|")
        negation_rep = replace_multiple(or_rep, negation_logic, "~")

        str1 = negation_rep.split("=")
        expression = str1[1].strip()

        # extract nodes from each logic expression and create one list
        logic_list = re.findall(r'\w+', negation_rep)

        logic_output = logic_list[0]
        logic_input = logic_list[1:]

        # cyclic node list
        if i in star_idx:
            cycle_node_list.append(logic_output)

        # remove duplicates in list
        logic_input = [x for i, x in enumerate(logic_input) if i == logic_input.index(x)]
        # print(logic_output, logic_input[0])

        for node in logic_input:

            # input negation
            if desired_attractor_dic[node] == "False":
                # exact replacement using regular expression
                expression = re.sub(r"\b" + node + r"\b", "( ~ " + node + ")", expression)

        # output negation
        if desired_attractor_dic[logic_output] == "False":
            expression = expression.replace(expression, " ~ ( " + expression + ")")

        # print(expression)
        expression_dnf = to_dnf(expression)

        # raw transformation
        plus_product_sep_raw = " | "
        x_raw = str(expression_dnf).split("|")
        plus_product_list = []
        for i in x_raw:
            plus_product_list.append(i.strip())
        term_selected_raw = plus_product_sep_raw.join(plus_product_list)
        transformed_logic_raw = logic_output + " = " + term_selected_raw
        format_transform_raw = format_transform_raw + transformed_logic_raw + "\n"


        # remain all plusproducts
        plus_product_sep = " | "
        x = str(expression_dnf).split("|")
        plus_product_list = []
        for i in x:
            if not ("~") in i:
                plus_product_list.append(i.strip())
        term_selected = plus_product_sep.join(plus_product_list)
        # print(term_selected)
        transformed_logic = logic_output + " = " + term_selected
        format_transform_all_plus_product = format_transform_all_plus_product + transformed_logic + "\n"

    G_net_raw = format_transform_raw
    G_net = format_transform_all_plus_product
    desired_attractor = desired_attractor
    cycle_node_list = cycle_node_list

    # replace the logics with symbols
    G_net = re.sub(r"\band\b", "&", G_net)
    G_net = re.sub(r"\bor\b", "|", G_net)
    G_net = re.sub(r"\bnot\s", "~", G_net)

    # get all nodes
    G_net_line = G_net.splitlines()
    G_net_dic = {}
    for line in G_net_line:
        state_variable = line.split("=")[0].strip()
        Boolean_expression = line.split("=")[1].strip()
        Boolean_expression_node_list = Boolean_expression.split(" | ")
        G_net_dic[state_variable] = Boolean_expression_node_list
    G_net_dic = dict(sorted(G_net_dic.items(), key=lambda kv: kv[0], reverse=False))

    # campare c and s
    M_1_sc_list = compare_c_and_s(initial_state, desired_attractor, G_net_dic)

    # list to dic
    M_1_sc_dic = {}
    for node in M_1_sc_list:
        M_1_sc_dic[node] = True

    # replace the logics with symbols
    G_net = G_net.replace("&", "and").replace("|", "or")

    # if cycle, remove cyclic nodes
    G_net = cyclic_node_remove(G_net, cycle_node_list)

    # remove monostable node
    G_net = remove_monostable_node(G_net)

    # G hat
    G_hat = canalizing(G_net, M_1_sc_dic)

    # all combi
    G_hat_one_plus = one_plus_prodcut(G_hat)[0]

    # get mFVSs
    solution = mFVSs(G_hat_one_plus)

    return solution




def compare_c_and_s(initial_state, desired_attractor, all_plus_product_net_dic):
    M_sc_list = []
    D_sc_list = []
    all_node_list = list(all_plus_product_net_dic.keys())
    for s, c, node in zip(initial_state, desired_attractor, all_node_list):
        if s == c:
            M_sc_list.append(node)
        else:
            D_sc_list.append(node)

    while True:
        M_1_sc_list = []
        for node in all_plus_product_net_dic:
            if node in M_sc_list:
                for plus_product in all_plus_product_net_dic[node]:
                    node_list = re.findall(r'\w+', plus_product)
                    same_check = True
                    for right_node in node_list:
                        if right_node not in M_sc_list:
                            same_check = False
                            break
                    if same_check == True:
                        break
                if same_check == True:
                    M_1_sc_list.append(node)
        if len(M_sc_list) == len(M_1_sc_list):
            break
        M_sc_list = M_1_sc_list.copy()


    # print(M_1_sc_list)
    return M_1_sc_list



def cyclic_node_remove(G_net, cycle_node_list):
    # split the G_net by line
    G_net_line = G_net.splitlines()

    G_net_new = ""
    for line in G_net_line:
        logic_list = line.split("=")
        logic_output = logic_list[0].strip()
        logic_input = logic_list[1].strip()

        if logic_output not in cycle_node_list:
            logic_input_list = logic_input.split(" or ")
            logic_input_list_extra = []
            for clause in logic_input_list:
                no_cycle_check = True
                for cycle_node in cycle_node_list:
                    if clause.find(cycle_node) != -1:
                        no_cycle_check = False
                        continue
                if no_cycle_check:
                    logic_input_list_extra.append(clause)

            logic_input_list_new = " or ".join(logic_input_list_extra)
            G_net_new += logic_output + " = " + logic_input_list_new + '\n'
    G_net = G_net_new.strip()

    return G_net



def all_combi(G_net):
    # Replace the logics with symbols
    G_net = re.sub(r"\band\b", "&", G_net)
    G_net = re.sub(r"\bor\b", "|", G_net)
    G_net = re.sub(r"\bnot\b", "~", G_net)
    lines = G_net.splitlines()

    possibleCombiList = []
    for line in lines:
        BooleanFunctionList = line.split("=")
        BooleanExpressionNodes = BooleanFunctionList[1].strip()
        SOPlist = BooleanExpressionNodes.split(" | ")
        if len(SOPlist) > 1:
            possibleCombiList.append(SOPlist)

    allCombiList = list(itertools.product(*possibleCombiList))

    G_net_list = []
    for i, combi in enumerate(allCombiList):
        G_net = ""
        num = 0
        for line in lines:
            BooleanFunctionList = line.split(" = ")
            stateVariable = BooleanFunctionList[0].strip()
            BooleanExpressionNodes = BooleanFunctionList[1].strip()
            SOPlist = BooleanExpressionNodes.split(" | ")

            if len(SOPlist) > 1:
                G_net = G_net + stateVariable + " = " + combi[num] + "\n"
                num += 1
            else:
                G_net = G_net + line + "\n"

        G_net = G_net.strip()
        G_net = G_net.replace("&", "and").replace("|", "or")
        G_net_list.append(G_net)

    return G_net_list
