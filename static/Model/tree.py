import json
import re
import pandas


def parse(newick):
    tokens = re.findall(r"([^:;,()\s]*)(?:\s*:\s*([\d.]+)\s*)?([,);])|(\S)", newick+";")

    def recurse(nextid = 0, parentid = -1): # one node
        thisid = nextid;
        children = []

        name, length, delim, ch = tokens.pop(0)
        if ch == "(":
            while ch in "(,":
                node, ch, nextid = recurse(nextid+1, thisid)
                children.append(node)
            name, length, delim, ch = tokens.pop(0)
        return {"id": thisid, "name": name, "length": float(length) if length else None,
                "parentid": parentid, "children": children}, delim, nextid

    return recurse()[0]


def recursive_tree_init(json_obj):
    num_of_children = len(json_obj[0].children)
    recursive_tree(json_obj, '' ,num_of_children)


def recursive_tree(json_obj, node_name, num_of_children):
    print(node_name + ',\n')

    while num_of_children > 0:
        recursive_tree(json_obj, json_obj[node_name].children[num_of_children], num_of_children-1)


if __name__ == '__main__':
    json_tree = json.dumps((parse("(smc,(esi,pin,pra,psj,pti),(((xbo,((bbe,bfl),(cin,csa,odi),(pma,(xla,xtr),(apl,"
                                  "cli,gga,tgu),(cfa,dno,ocu,(aja,eca,efu,pal),(mdo,meu,sha),((age,lla),(cja,sbo,"
                                  "sla),(mml,mne,pbi,pha),mmr,dma,oga,(ggo,hsa,ppa,ppy,ptr,ssy),nle,lca),oan,(cgr,"
                                  "cpo,mmu,rno),(bta,chi,oar),tch,ssc),(aca,ami,cpi,oha,pbv),(abu,ccr,dre,eel,fru,"
                                  "gmo,hhi,ipu,mze,nbr,ola,oni,pny,pol,ssa,tni))),(lva,pmi,spu),sko),(((isc,pte,rmi,"
                                  "tur),(dpu,mja,tcf),(aae,aga,ame,api,bdo,bib,bmo,cqu,dan,der,dgr,dme,dmo,dpe,dps,"
                                  "dqu,dse,dsi,dvi,dwi,dya,hme,lmi,mse,ngi,nlo,nvi,pca,pxy,sfr,tca),smr),(asu,bma,"
                                  "cbn,cbr,cel,crm,hco,hpo,ppc,prd,str)),(cte,(gpy,tre),(hru,lgi,mle),cla,(egr,emu,"
                                  "fhe,gsa,mco,sja,sma,sme))),(hma,nve),(aqu,lco,sci)),ddi,(cre,(cln,pab,pde,pta),"
                                  "(ppt,smo),(atr,(seu,pgi,(cca,han,har,hci,hex,hpa,hpe,htu),(aly,ath,bna,bol,bra,"
                                  "cas),cpa,(cme,cst),(hbr,mes,rco),(aau,ahy,amg,gma,gso,lja,mtr,pvu,vun),(ama,dpr,"
                                  "rgl,smi,ssl),lus,(gar,ghb,ghr,gra,tcc),eun,pla,aqc,(bcy,bgy),(fve,mdm,ppe),(ccl,"
                                  "crt,csi,ctr),(peu,ptc),(nta,sly,stu),vvi),(aof,ata,bdi,egu,far,hvu,osa,sbi,sof,"
                                  "ssp,tae,ttu,vca,zma))),(bfv,bhv1,bhv5,bkv,blv,bpcv1,bpcv2,dev,ebv,gggpv1,hbv,hcmv,"
                                  "hhv6b,hiv1,hsv1,hsv2,hvsa,hvt,iltv,jcv,kshv,mcmv,mcpv,mdv1,mdv2,mghv,prv,ptvpv2a,"
                                  "racpv,rlcv,rrv,sfv,sv40,ttv));")
                     ))
    print(json_tree[1])

    # df = pandas.read_json(json_tree)
    # csv_file = df.to_csv()
    # with open('test.csv', 'w') as file:
    #     file.write(csv_file)
