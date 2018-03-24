# 利用个人的基因数据计算亲属关系

平台OS X (64-bit)

## [PLINK](http://www.cog-genomics.org/plink/1.9/)

基于PLINK 1.90 beta。

### 处理数据

如果数据不是 PLINK 格式（`*.ped` 和 `*.map`），需要转化为这种格式。

#### 转化

如果数据是 23andme 的格式，你需要使用 [Python](http://www.jade-cheng.com/au/23andme-to-plink/23andme-to-plink.py) 程序进行转化成 PLINK 格式，本项目运行于 [Python 3.6.4](https://www.python.org/downloads/release/python-364/)。

```cmd
python3 23andme_to_plink.py [-h] [--gender [GENDER]] path

```

转换之后的格式为 `*.ped` 和 `*.map`。

例如：

```cmd
python3 23andme_to_plink.py user_1.txt
```

结果生成`user_1.ped`和`user_1.map`。

可以使用下面的命令进一步转化为二进制文件(`*.bed`、`*.fam` 、`*.bim`)：

```cmd
plink --file [filename] --make-bed
```

### 合并

计算亲属关系需要关联多个人的基因数据。

不同人的多个文件需要合并为一个文件。查看[合并](http://www.cog-genomics.org/plink/1.9/data#merge_list)的更多消息

```cmd
plink --file [filename1] --merge-list merge.txt --make-bed --out mydata
```

`[filename1]`为基准文件，与其他人的数据合并。

`--merge-list merge.txt`为需要合并的其他人的文件列表，格式为：

```
user_2.ped user_2.map
user_3.ped user_3.map
```

如果`--out mydata`默认输出 mydata 文件名的相关数据，否则默认为 plink 文件名。

例如：

```cmd
./plink --file user_1 --merge-list merge.txt --out mydata
```

## 使用 King 计算亲属关系


[KING 2.1.3](http://people.virginia.edu/~wc9c/KING/Download.htm) 下载地址。亲属关系系数使用下面的命令行计算。

 ```cmd
king -b [filename.bed] –-kinship
```

为了找到亲属关系系数，使用以下命令：

```cmd
cat king.kin0
```

例如：

```cmd
./king -b mydata.bed --kinship
```

这是一个样例的结果:

    FID1	ID1	FID2	ID2	N_SNP	HetHet	IBS0	Kinship
    user_1_FAM	user_1	user_2_FAM	user_2	503447	0.1434	0.0001	0.2494
    user_1_FAM	user_1	user_3_FAM	user_3	505956	0.1130	0.0563	-0.0018
    user_2_FAM	user_2	user_3_FAM	user_3	564572	0.1017	0.0510	-0.0028

如何解释这些结果呢？

上述结果（最后一栏）报告的“亲属关系”是亲属关系系数。在第二列的下表中查找该值。为了区分亲缘关系和完全兄弟关系，两者的亲缘系数大约为0.25，请在倒数第二列中查找上面的 IBS0 值。

## 使用 SNPRelate 计算亲属关系

### 安装

#### 安装R

[R 镜像列表](https://cran.r-project.org/mirrors.html)

[R China 中科大镜像](https://mirrors.ustc.edu.cn/CRAN/)，下载 R-3.4.4版本安装。

#### 安装 SNPRelate

一个 R 包, [SNPRelate](https://bioconductor.org/packages/release/bioc/html/SNPRelate.html)。

启动R，运行下面的命令：

```cmd
## try http:// if https:// URLs are not supported
source("https://bioconductor.org/biocLite.R")
biocLite("SNPRelate")
```

或者直接下载对应的安装包，通过 R GUI 窗口安装包。

+ 打开工具栏 packages&data
+ package install
+ 选择 packages repoitory(bioconductor(binaries))
+ get list 同时勾选右下角 install dependencies
+ 搜索 SNPRelate 安装

![install](/pictrue/Snipaste_2018-03-24_16-41-10.png)

### 生成 gds 数据

SNPRelate 使用自有的 gds 数据格式。可以使用下面命令将 PLINK 的二进制数据文件转化为 gds 数据格式。
启动 R，加载 SNPRelate：`library(SNPRelate)`

```cmd
bed.fn <- "mydata.bed"
fam.fn <- "mydata.fam"
bim.fn <- "mydata.bim"
snpgdsBED2GDS(bed.fn, fam.fn, bim.fn, "mydata.gds")
```

使用 SNPRelate 的好处是可以多种亲属关系方法，包括 PLINK 和 KING。

### 使用 PLINK

```cmd
mydata <- snpgdsOpen("mydata.gds")
ibd.plink <- snpgdsIBDMoM(mydata, num.thread=4)
ibd.plink.coeff <- snpgdsIBDSelection(ibd.plink)
ibd.plink.coeff
```

结果:

        ID1    ID2 k0 k1 kinship
    1 user_1 user_2  0  1    0.25
    2 user_1 user_3  1  0    0.00
    3 user_2 user_3  1  0    0.00

### 使用 KING

```cmd
ibd.king <- snpgdsIBDKING(mydata, num.thread=4)
ibd.king.coeff <- snpgdsIBDSelection(ibd.king)
ibd.king.coeff
```

结果:

        ID1    ID2         IBS0      kinship
    1 user_1 user_2 0.0001281758  0.249388639
    2 user_1 user_3 0.0983487733 -0.001762033

如上所示，两种方法结论高度相式的。
