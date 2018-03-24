# 利用个人的基因数据计算亲属关系

## 数据格式的变化和合并

如果数据不是 PLINK 格式，需要转化为这种格式。

mycodon 格式转化为 PLINK 格式：
```cmd
python3 mycodon_to_plink.py [-h] [--gender [GENDER]] path

```

如果数据是 23andme 的格式，你需要使用 [Python](http://www.jade-cheng.com/au/23andme-to-plink/23andme-to-plink.py) 程序进行转化成 PLINK 格式

转换之后的格式为 `*.ped` 和 `*.map`。他们需要使用下面的命令转化为二进制文件(`*.bed`、`*.fam` 、`*.bim`)：
```cmd
plink --file [filename] --make-bed
```

不同人的多个文件需要合并为一个文件。查看[合并](http://zzz.bwh.harvard.edu/plink/dataman.shtml#mergelist)的更多消息

```cmd
plink --file [filename1] --merge-list allfiles.txt --make-bed --out mynewdata
```

## 使用 King 计算亲属关系


[KING](http://people.virginia.edu/~wc9c/KING/Download.htm) 下载地址。亲属关系系数使用下面的命令行计算。
 ```cmd
king -b [filename.bed] –-kinship
```

为了找到亲属关系系数，使用以下命令：


```cmd
cat king.kin0
```

这是一个样例的结果:

    FID1	            ID1	           FID2	               ID2	        N_SNP  HetHet IBS0	Kinship 
    20170213024839_FAM 20170213024839 20170213040746_FAM 20170213040746 503447 0.1434 0.0001 0.2494
    20170213024839_FAM 20170213024839 20171118172353_FAM 20171118172353 505956 0.1130 0.0563 -0.0018
    20170213040746_FAM 20170213040746 20171118172353_FAM 20171118172353 564572 0.1017 0.0510 -0.0028

如何解释这些结果呢？

上述结果（最后一栏）报告的“亲属关系”是亲属关系系数。 
在第二列的下表中查找该值。 
为了区分亲缘关系和完全兄弟关系，两者的亲缘系数大约为0.25，请在倒数第二列中查找上面的 IBS0 值。

 
## 使用 SNPRelate 计算亲属关系

一个 R 包, [SNPRelate](https://bioconductor.org/packages/release/bioc/html/SNPRelate.html).

SNPRelate 使用自有的 gds 数据格式。可以使用下面命令将 PLINK 的二进制数据文件转化为 gds 数据格式。
 
```
bed.fn <- "plink_file.bed" 
fam.fn <- "plink_file.fam" 
bim.fn <- "plink_file.bim"
snpgdsBED2GDS(bed.fn, fam.fn, bim.fn, "filename.gds")
```
使用 SNPRelate 的好处是可以多种亲属关系方法，包括 PLINK 和 KING。

### 使用 PLINK:

```cmd
example <- snpgdsOpen("example.gds")
ibd.plink <- snpgdsIBDMoM(example, num.thread=4) 
ibd.plink.coeff <- snpgdsIBDSelection(ibd.plink) 
ibd.plink.coeff
```

结果:		

                ID1         ID2        k0  k1   kinship
    1	20170213024839	20170213040746	0	1	0.25
    2	20170213024839	20171118172353	1	0	0.00
    3	20170213040746	20171118172353	1	0	0.00


### 使用 KING
```cmd
ibd.king <- snpgdsIBDKING(example, num.thread=4) 
ibd.king.coeff <- snpgdsIBDSelection(ibd.king) 
ibd.king.coeff

```

结果:
 
         ID1	             ID2	         IBS0	         kinship
    1	20170213024839	20170213040746	0.0001281758	0.249388639
    2	20170213024839	20171118172353	0.0983487733	-0.001762033
    3	20170213040746	20171118172353	0.0986352761	-0.002795260


如上所示，两种方法结论高度相式的。

