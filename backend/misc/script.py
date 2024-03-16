"""script to convert table html to json"""
from bs4 import BeautifulSoup
from csv import writer
table_html = """<tbody>
    <tr class="row-2 even">
        <td class="column-1">NS10</td>
        <td class="column-2">Admiralty</td>
        <td class="column-3">海军部</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-3 odd">
        <td class="column-1">EW9</td>
        <td class="column-2">Aljunied</td>
        <td class="column-3">阿裕尼</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-4 even">
        <td class="column-1">NS16</td>
        <td class="column-2">Ang Mo Kio</td>
        <td class="column-3">宏茂桥</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-5 odd">
        <td class="column-1">CR2</td>
        <td class="column-2">Aviation Park</td>
        <td class="column-3">航空园</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-6 even">
        <td class="column-1">JS7</td>
        <td class="column-2">Bahar Junction</td>
        <td class="column-3">峇哈路口</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-7 odd">
        <td class="column-1">SE3</td>
        <td class="column-2">Bakau</td>
        <td class="column-3">码高</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-8 even">
        <td class="column-1">BP9</td>
        <td class="column-2">Bangkit</td>
        <td class="column-3">万吉</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-9 odd">
        <td class="column-1">CC12</td>
        <td class="column-2">Bartley</td>
        <td class="column-3">巴特礼</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-10 even">
        <td class="column-1">DT16</td>
        <td class="column-2">Bayfront</td>
        <td class="column-3">海湾舫</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-11 odd">
        <td class="column-1">CE1</td>
        <td class="column-2">Bayfront</td>
        <td class="column-3">海湾舫</td>
        <td class="column-4">Circle Line Extension</td>
        <td class="column-5">环线延长线</td>
    </tr>
    <tr class="row-12 even">
        <td class="column-1">TE29</td>
        <td class="column-2">Bayshore</td>
        <td class="column-3">碧湾</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-13 odd">
        <td class="column-1">DT5</td>
        <td class="column-2">Beauty World</td>
        <td class="column-3">美世界</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-14 even">
        <td class="column-1">EW5</td>
        <td class="column-2">Bedok</td>
        <td class="column-3">勿洛</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-15 odd">
        <td class="column-1">DT29</td>
        <td class="column-2">Bedok North</td>
        <td class="column-3">勿洛北</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-16 even">
        <td class="column-1">DT30</td>
        <td class="column-2">Bedok Reservoir</td>
        <td class="column-3">勿洛蓄水池</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-17 odd">
        <td class="column-1">TE30</td>
        <td class="column-2">Bedok South</td>
        <td class="column-3">勿洛南</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-18 even">
        <td class="column-1">DT21</td>
        <td class="column-2">Bencoolen</td>
        <td class="column-3">明古连</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-19 odd">
        <td class="column-1">DT23</td>
        <td class="column-2">Bendemeer</td>
        <td class="column-3">明地迷亚</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-20 even">
        <td class="column-1">NS17</td>
        <td class="column-2">Bishan</td>
        <td class="column-3">碧山</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-21 odd">
        <td class="column-1">CC15</td>
        <td class="column-2">Bishan</td>
        <td class="column-3">碧山</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-22 even">
        <td class="column-1">NE9</td>
        <td class="column-2">Boon Keng</td>
        <td class="column-3">文庆</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-23 odd">
        <td class="column-1">EW27 / JS8</td>
        <td class="column-2">Boon Lay</td>
        <td class="column-3">文礼</td>
        <td class="column-4">East West Line / Jurong Region Line</td>
        <td class="column-5">东西线 / 裕廊区域线</td>
    </tr>
    <tr class="row-24 even">
        <td class="column-1">DT9</td>
        <td class="column-2">Botanic Gardens</td>
        <td class="column-3">植物园</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-25 odd">
        <td class="column-1">CC19</td>
        <td class="column-2">Botanic Gardens</td>
        <td class="column-3">植物园</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-26 even">
        <td class="column-1">NS18</td>
        <td class="column-2">Braddell</td>
        <td class="column-3">布莱德</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-27 odd">
        <td class="column-1">CC2</td>
        <td class="column-2">Bras Basah</td>
        <td class="column-3">百胜</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-28 even">
        <td class="column-1">TE7</td>
        <td class="column-2">Bright Hill</td>
        <td class="column-3">光明山</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-29 odd">
        <td class="column-1">NE15</td>
        <td class="column-2">Buangkok</td>
        <td class="column-3">万国</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-30 even">
        <td class="column-1">EW12</td>
        <td class="column-2">Bugis</td>
        <td class="column-3">武吉士</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-31 odd">
        <td class="column-1">DT14</td>
        <td class="column-2">Bugis</td>
        <td class="column-3">武吉士</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-32 even">
        <td class="column-1">NS2</td>
        <td class="column-2">Bukit Batok</td>
        <td class="column-3">武吉巴督</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-33 odd">
        <td class="column-1">JE3</td>
        <td class="column-2">Bukit Batok West</td>
        <td class="column-3">武吉巴督西</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-34 even">
        <td class="column-1">NS3</td>
        <td class="column-2">Bukit Gombak</td>
        <td class="column-3">武吉甘柏</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-35 odd">
        <td class="column-1">DT1</td>
        <td class="column-2">Bukit Panjang</td>
        <td class="column-3">武吉班让</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-36 even">
        <td class="column-1">BP6</td>
        <td class="column-2">Bukit Panjang</td>
        <td class="column-3">武吉班让</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-37 odd">
        <td class="column-1">EW21</td>
        <td class="column-2">Buona Vista</td>
        <td class="column-3">波那维斯达</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-38 even">
        <td class="column-1">CC22</td>
        <td class="column-2">Buona Vista</td>
        <td class="column-3">波那维斯达</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-39 odd">
        <td class="column-1">CC17</td>
        <td class="column-2">Caldecott</td>
        <td class="column-3">加利谷</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-40 even">
        <td class="column-1">TE9</td>
        <td class="column-2">Caldecott</td>
        <td class="column-3">加利谷</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-41 odd">
        <td class="column-1">DT2</td>
        <td class="column-2">Cashew</td>
        <td class="column-3">凯秀</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-42 even">
        <td class="column-1">CG2</td>
        <td class="column-2">Changi Airport</td>
        <td class="column-3">樟宜机场</td>
        <td class="column-4">Changi Airport Branch Line</td>
        <td class="column-5">樟宜机场支线</td>
    </tr>
    <tr class="row-43 odd">
        <td class="column-1">SW1</td>
        <td class="column-2">Cheng Lim</td>
        <td class="column-3">振林</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-44 even">
        <td class="column-1">NE4</td>
        <td class="column-2">Chinatown</td>
        <td class="column-3">牛车水</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-45 odd">
        <td class="column-1">DT19</td>
        <td class="column-2">Chinatown</td>
        <td class="column-3">牛车水</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-46 even">
        <td class="column-1">EW25</td>
        <td class="column-2">Chinese Garden</td>
        <td class="column-3">裕华园</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-47 odd">
        <td class="column-1">NS4</td>
        <td class="column-2">Choa Chu Kang</td>
        <td class="column-3">蔡厝港</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-48 even">
        <td class="column-1">BP1</td>
        <td class="column-2">Choa Chu Kang</td>
        <td class="column-3">蔡厝港</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-49 odd">
        <td class="column-1">JS2</td>
        <td class="column-2">Choa Chu Kang West</td>
        <td class="column-3">蔡厝港西</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-50 even">
        <td class="column-1">NS25</td>
        <td class="column-2">City Hall</td>
        <td class="column-3">政府大厦</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-51 odd">
        <td class="column-1">EW13</td>
        <td class="column-2">City Hall</td>
        <td class="column-3">政府大厦</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-52 even">
        <td class="column-1">NE5</td>
        <td class="column-2">Clarke Quay</td>
        <td class="column-3">克拉码头</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-53 odd">
        <td class="column-1">EW23</td>
        <td class="column-2">Clementi</td>
        <td class="column-3">金文泰</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-54 even">
        <td class="column-1">EW20</td>
        <td class="column-2">Commonwealth</td>
        <td class="column-3">联邦</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-55 odd">
        <td class="column-1">SE1</td>
        <td class="column-2">Compassvale</td>
        <td class="column-3">康埔桦</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-56 even">
        <td class="column-1">PE3</td>
        <td class="column-2">Coral Edge</td>
        <td class="column-3">珊瑚</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-57 odd">
        <td class="column-1">JS5</td>
        <td class="column-2">Corporation</td>
        <td class="column-3">企业</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-58 even">
        <td class="column-1">PE1</td>
        <td class="column-2">Cove</td>
        <td class="column-3">海湾</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-59 odd">
        <td class="column-1">CC8</td>
        <td class="column-2">Dakota</td>
        <td class="column-3">达科达</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-60 even">
        <td class="column-1">PE7</td>
        <td class="column-2">Damai</td>
        <td class="column-3">达迈</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-61 odd">
        <td class="column-1">CR7</td>
        <td class="column-2">Defu</td>
        <td class="column-3">德福</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-62 even">
        <td class="column-1">NS24</td>
        <td class="column-2">Dhoby Ghaut</td>
        <td class="column-3">多美歌</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-63 odd">
        <td class="column-1">NE6</td>
        <td class="column-2">Dhoby Ghaut</td>
        <td class="column-3">多美歌</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-64 even">
        <td class="column-1">CC1</td>
        <td class="column-2">Dhoby Ghaut</td>
        <td class="column-3">多美歌</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-65 odd">
        <td class="column-1">EW22</td>
        <td class="column-2">Dover</td>
        <td class="column-3">杜弗</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-66 even">
        <td class="column-1">DT17</td>
        <td class="column-2">Downtown</td>
        <td class="column-3">市中心</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-67 odd">
        <td class="column-1">CP2</td>
        <td class="column-2">Elias</td>
        <td class="column-3">伊莱雅</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-68 even">
        <td class="column-1">JS9</td>
        <td class="column-2">Enterprise</td>
        <td class="column-3">事业</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-69 odd">
        <td class="column-1">CC3</td>
        <td class="column-2">Esplanade</td>
        <td class="column-3">滨海中心</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-70 even">
        <td class="column-1">EW7</td>
        <td class="column-2">Eunos</td>
        <td class="column-3">友诺士</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-71 odd">
        <td class="column-1">DT35</td>
        <td class="column-2">Expo</td>
        <td class="column-3">博览</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-72 even">
        <td class="column-1">CG1</td>
        <td class="column-2">Expo</td>
        <td class="column-3">博览</td>
        <td class="column-4">Changi Airport Branch Line</td>
        <td class="column-5">樟宜机场支线</td>
    </tr>
    <tr class="row-73 odd">
        <td class="column-1">BP10</td>
        <td class="column-2">Fajar</td>
        <td class="column-3">法嘉</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-74 even">
        <td class="column-1">SW2</td>
        <td class="column-2">Farmway</td>
        <td class="column-3">农道</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-75 odd">
        <td class="column-1">NE8</td>
        <td class="column-2">Farrer Park</td>
        <td class="column-3">花拉公园</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-76 even">
        <td class="column-1">CC20</td>
        <td class="column-2">Farrer Road</td>
        <td class="column-3">花拉路</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-77 odd">
        <td class="column-1">SW5</td>
        <td class="column-2">Fernvale</td>
        <td class="column-3">芬微</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-78 even">
        <td class="column-1">DT20</td>
        <td class="column-2">Fort Canning</td>
        <td class="column-3">福康宁</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-79 odd">
        <td class="column-1">TE22A</td>
        <td class="column-2">Founders' Memorial</td>
        <td class="column-3">建国先贤纪念园</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-80 even">
        <td class="column-1">TE22</td>
        <td class="column-2">Gardens by The Bay</td>
        <td class="column-3">滨海湾花园</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-81 odd">
        <td class="column-1">JW1</td>
        <td class="column-2">Gek Poh</td>
        <td class="column-3">玉宝</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-82 even">
        <td class="column-1">DT24</td>
        <td class="column-2">Geylang Bahru</td>
        <td class="column-3">芽笼峇鲁</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-83 odd">
        <td class="column-1">TE15</td>
        <td class="column-2">Great World</td>
        <td class="column-3">大世界</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-84 even">
        <td class="column-1">EW30</td>
        <td class="column-2">Gul Circle</td>
        <td class="column-3">卡尔圈 站</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-85 odd">
        <td class="column-1">NE1</td>
        <td class="column-2">HarbourFront</td>
        <td class="column-3">港湾</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-86 even">
        <td class="column-1">CC29</td>
        <td class="column-2">HarbourFront</td>
        <td class="column-3">港湾</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-87 odd">
        <td class="column-1">TE16</td>
        <td class="column-2">Havelock</td>
        <td class="column-3">合乐</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-88 even">
        <td class="column-1">CC25</td>
        <td class="column-2">Haw Par Villa</td>
        <td class="column-3">虎豹别墅</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-89 odd">
        <td class="column-1">DT3</td>
        <td class="column-2">Hillview</td>
        <td class="column-3">山景</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-90 even">
        <td class="column-1">CC21</td>
        <td class="column-2">Holland Village</td>
        <td class="column-3">荷兰村</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-91 odd">
        <td class="column-1">JS4</td>
        <td class="column-2">Hong Kah</td>
        <td class="column-3">丰加</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-92 even">
        <td class="column-1">NE14</td>
        <td class="column-2">Hougang</td>
        <td class="column-3">后港</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-93 odd">
        <td class="column-1">DT22</td>
        <td class="column-2">Jalan Besar</td>
        <td class="column-3">惹兰勿刹</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-94 even">
        <td class="column-1">BP12</td>
        <td class="column-2">Jelapang</td>
        <td class="column-3">泽拉邦</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-95 odd">
        <td class="column-1">EW29</td>
        <td class="column-2">Joo Koon</td>
        <td class="column-3">裕群</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-96 even">
        <td class="column-1">NS1</td>
        <td class="column-2">Jurong East</td>
        <td class="column-3">裕廊东</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-97 odd">
        <td class="column-1">EW24</td>
        <td class="column-2">Jurong East</td>
        <td class="column-3">裕廊东</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-98 even">
        <td class="column-1">JS11</td>
        <td class="column-2">Jurong Hill</td>
        <td class="column-3">裕廊山</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-99 odd">
        <td class="column-1">CR19</td>
        <td class="column-2">Jurong Lake District</td>
        <td class="column-3">裕廊湖区</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-100 even">
        <td class="column-1">JS12</td>
        <td class="column-2">Jurong Pier</td>
        <td class="column-3">裕廊渡头</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-101 odd">
        <td class="column-1">JE6</td>
        <td class="column-2">Jurong Town Hall</td>
        <td class="column-3">裕廊镇大会堂</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-102 even">
        <td class="column-1">JS6</td>
        <td class="column-2">Jurong West</td>
        <td class="column-3">裕廊西</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-103 odd">
        <td class="column-1">PE5</td>
        <td class="column-2">Kadaloor</td>
        <td class="column-3">卡达鲁</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-104 even">
        <td class="column-1">DT28</td>
        <td class="column-2">Kaki Bukit</td>
        <td class="column-3">加基武吉</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-105 odd">
        <td class="column-1">EW10</td>
        <td class="column-2">Kallang</td>
        <td class="column-3">加冷</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-106 even">
        <td class="column-1">SE4</td>
        <td class="column-2">Kangkar</td>
        <td class="column-3">港脚</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-107 odd">
        <td class="column-1">TE24</td>
        <td class="column-2">Katong Park</td>
        <td class="column-3">加东公园</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-108 even">
        <td class="column-1">BP3</td>
        <td class="column-2">Keat Hong</td>
        <td class="column-3">吉丰</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-109 odd">
        <td class="column-1">EW6</td>
        <td class="column-2">Kembangan</td>
        <td class="column-3">景万岸</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-110 even">
        <td class="column-1">CC24</td>
        <td class="column-2">Kent Ridge</td>
        <td class="column-3">肯特岗</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-111 odd">
        <td class="column-1">NS14</td>
        <td class="column-2">Khatib</td>
        <td class="column-3">卡迪</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-112 even">
        <td class="column-1">DT6</td>
        <td class="column-2">King Albert Park</td>
        <td class="column-3">阿尔柏王园</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-113 odd">
        <td class="column-1">NE13</td>
        <td class="column-2">Kovan</td>
        <td class="column-3">高文</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-114 even">
        <td class="column-1">NS7</td>
        <td class="column-2">Kranji</td>
        <td class="column-3">克兰芝</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-115 odd">
        <td class="column-1">SW3</td>
        <td class="column-2">Kupang</td>
        <td class="column-3">古邦</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-116 even">
        <td class="column-1">CC27</td>
        <td class="column-2">Labrador Park</td>
        <td class="column-3">拉柏多公园</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-117 odd">
        <td class="column-1">EW26</td>
        <td class="column-2">Lakeside</td>
        <td class="column-3">湖畔</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-118 even">
        <td class="column-1">EW11</td>
        <td class="column-2">Lavender</td>
        <td class="column-3">劳明达</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-119 odd">
        <td class="column-1">SW6</td>
        <td class="column-2">Layar</td>
        <td class="column-3">拉雅</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-120 even">
        <td class="column-1">TE5</td>
        <td class="column-2">Lentor</td>
        <td class="column-3">伦多</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-121 odd">
        <td class="column-1">NE7</td>
        <td class="column-2">Little India</td>
        <td class="column-3">小印度</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-122 even">
        <td class="column-1">DT12</td>
        <td class="column-2">Little India</td>
        <td class="column-3">小印度</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-123 odd">
        <td class="column-1">CC14</td>
        <td class="column-2">Lorong Chuan</td>
        <td class="column-3">罗弄泉</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-124 even">
        <td class="column-1">CR3</td>
        <td class="column-2">Loyang</td>
        <td class="column-3">罗央</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-125 odd">
        <td class="column-1">DT26</td>
        <td class="column-2">MacPherson</td>
        <td class="column-3">麦波申</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-126 even">
        <td class="column-1">CC10</td>
        <td class="column-2">MacPherson</td>
        <td class="column-3">麦波申</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-127 odd">
        <td class="column-1">CR16</td>
        <td class="column-2">Maju</td>
        <td class="column-3">马裕</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-128 even">
        <td class="column-1">NS27</td>
        <td class="column-2">Marina Bay</td>
        <td class="column-3">滨海湾</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-129 odd">
        <td class="column-1">CE2</td>
        <td class="column-2">Marina Bay</td>
        <td class="column-3">滨海湾</td>
        <td class="column-4">Circle Line Extension</td>
        <td class="column-5">环线延长线</td>
    </tr>
    <tr class="row-130 even">
        <td class="column-1">TE20</td>
        <td class="column-2">Marina Bay</td>
        <td class="column-3">滨海湾</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-131 odd">
        <td class="column-1">TE21</td>
        <td class="column-2">Marina South</td>
        <td class="column-3">滨海南</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-132 even">
        <td class="column-1">NS28</td>
        <td class="column-2">Marina South Pier</td>
        <td class="column-3">滨海南码头</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-133 odd">
        <td class="column-1">TE26</td>
        <td class="column-2">Marine Parade</td>
        <td class="column-3">马林百列</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-134 even">
        <td class="column-1">TE27</td>
        <td class="column-2">Marine Terrace</td>
        <td class="column-3">马林台</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-135 odd">
        <td class="column-1">NS8</td>
        <td class="column-2">Marsiling</td>
        <td class="column-3">马西岭</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-136 even">
        <td class="column-1">CC16</td>
        <td class="column-2">Marymount</td>
        <td class="column-3">玛丽蒙</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-137 odd">
        <td class="column-1">DT25</td>
        <td class="column-2">Mattar</td>
        <td class="column-3">玛达</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-138 even">
        <td class="column-1">TE18</td>
        <td class="column-2">Maxwell</td>
        <td class="column-3">麦士威</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-139 odd">
        <td class="column-1">TE6</td>
        <td class="column-2">Mayflower</td>
        <td class="column-3">美华</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-140 even">
        <td class="column-1">PE2</td>
        <td class="column-2">Meridian</td>
        <td class="column-3">丽园</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-141 odd">
        <td class="column-1">TE10</td>
        <td class="column-2">Mount Pleasant</td>
        <td class="column-3">快乐山</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-142 even">
        <td class="column-1">CC7</td>
        <td class="column-2">Mountbatten</td>
        <td class="column-3">蒙巴登</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-143 odd">
        <td class="column-1">JW4</td>
        <td class="column-2">Nanyang Crescent</td>
        <td class="column-3">南洋弯</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-144 even">
        <td class="column-1">JW3</td>
        <td class="column-2">Nanyang Gateway</td>
        <td class="column-3">南洋门</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-145 odd">
        <td class="column-1">TE12</td>
        <td class="column-2">Napier</td>
        <td class="column-3">纳比雅</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-146 even">
        <td class="column-1">NS21</td>
        <td class="column-2">Newton</td>
        <td class="column-3">纽顿</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-147 odd">
        <td class="column-1">DT11</td>
        <td class="column-2">Newton</td>
        <td class="column-3">纽顿</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-148 even">
        <td class="column-1">PW5</td>
        <td class="column-2">Nibong</td>
        <td class="column-3">尼蒙</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-149 odd">
        <td class="column-1">CC5</td>
        <td class="column-2">Nicoll Highway</td>
        <td class="column-3">尼诰大道</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-150 even">
        <td class="column-1">NS20</td>
        <td class="column-2">Novena</td>
        <td class="column-3">诺维娜</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-151 odd">
        <td class="column-1">PE6</td>
        <td class="column-2">Oasis</td>
        <td class="column-3">绿洲</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-152 even">
        <td class="column-1">CC23</td>
        <td class="column-2">one-north</td>
        <td class="column-3">纬壹</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-153 odd">
        <td class="column-1">NS22</td>
        <td class="column-2">Orchard</td>
        <td class="column-3">乌节</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-154 even">
        <td class="column-1">TE14</td>
        <td class="column-2">Orchard</td>
        <td class="column-3">乌节</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-155 odd">
        <td class="column-1">TE13</td>
        <td class="column-2">Orchard Boulevard</td>
        <td class="column-3">乌节大道</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-156 even">
        <td class="column-1">NE3</td>
        <td class="column-2">Outram Park</td>
        <td class="column-3">欧南园</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-157 odd">
        <td class="column-1">EW16</td>
        <td class="column-2">Outram Park</td>
        <td class="column-3">欧南园</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-158 even">
        <td class="column-1">TE17</td>
        <td class="column-2">Outram Park</td>
        <td class="column-3">欧南园</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-159 odd">
        <td class="column-1">JE7</td>
        <td class="column-2">Pandan Reservoir</td>
        <td class="column-3">班丹蓄水池</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-160 even">
        <td class="column-1">CC26</td>
        <td class="column-2">Pasir Panjang</td>
        <td class="column-3">巴西班让</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-161 odd">
        <td class="column-1">EW1</td>
        <td class="column-2">Pasir Ris</td>
        <td class="column-3">巴西立</td>
        <td class="column-4">East West Line / Cross Island Line</td>
        <td class="column-5">东西线 / 跨岛地铁线</td>
    </tr>
    <tr class="row-162 even">
        <td class="column-1">CR4</td>
        <td class="column-2">Pasir Ris East</td>
        <td class="column-3">巴西立东</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-163 odd">
        <td class="column-1">EW8</td>
        <td class="column-2">Paya Lebar</td>
        <td class="column-3">巴耶利峇</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-164 even">
        <td class="column-1">CC9</td>
        <td class="column-2">Paya Lebar</td>
        <td class="column-3">巴耶利峇</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-165 odd">
        <td class="column-1">BP8</td>
        <td class="column-2">Pending</td>
        <td class="column-3">秉定</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-166 even">
        <td class="column-1">JW5</td>
        <td class="column-2">Peng Kang Hill</td>
        <td class="column-3">秉光山</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-167 odd">
        <td class="column-1">BP7</td>
        <td class="column-2">Petir</td>
        <td class="column-3">柏提</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-168 even">
        <td class="column-1">BP5</td>
        <td class="column-2">Phoenix</td>
        <td class="column-3">凤凰</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-169 odd">
        <td class="column-1">EW28</td>
        <td class="column-2">Pioneer</td>
        <td class="column-3">先驱</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-170 even">
        <td class="column-1">NE10</td>
        <td class="column-2">Potong Pasir</td>
        <td class="column-3">波东巴西</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-171 odd">
        <td class="column-1">DT15</td>
        <td class="column-2">Promenade</td>
        <td class="column-3">宝门廊</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-172 even">
        <td class="column-1">CC4</td>
        <td class="column-2">Promenade</td>
        <td class="column-3">宝门廊</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-173 odd">
        <td class="column-1">CP4 / NE17 / PTC</td>
        <td class="column-2">Punggol</td>
        <td class="column-3">榜鹅</td>
        <td class="column-4">Cross Island Line / North East Line / Punggol LRT</td>
        <td class="column-5">跨岛地铁线 / 东北线 / 榜鹅轻轨线</td>
    </tr>
    <tr class="row-174 even">
        <td class="column-1">PW3</td>
        <td class="column-2">Punggol Point</td>
        <td class="column-3">榜鹅坊</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-175 odd">
        <td class="column-1">EW19</td>
        <td class="column-2">Queenstown</td>
        <td class="column-3">女皇镇</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-176 even">
        <td class="column-1">NS26</td>
        <td class="column-2">Raffles Place</td>
        <td class="column-3">莱佛士坊</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-177 odd">
        <td class="column-1">EW14</td>
        <td class="column-2">Raffles Place</td>
        <td class="column-3">莱佛士坊</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-178 even">
        <td class="column-1">SE5</td>
        <td class="column-2">Ranggung</td>
        <td class="column-3">兰岗</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-179 odd">
        <td class="column-1">EW18</td>
        <td class="column-2">Redhill</td>
        <td class="column-3">红山</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-180 even">
        <td class="column-1">SW8</td>
        <td class="column-2">Renjong</td>
        <td class="column-3">仁宗</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-181 odd">
        <td class="column-1">PE4</td>
        <td class="column-2">Riviera</td>
        <td class="column-3">里维拉</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-182 even">
        <td class="column-1">CP3</td>
        <td class="column-2">Riviera</td>
        <td class="column-3">里维拉</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-183 odd">
        <td class="column-1">DT13</td>
        <td class="column-2">Rochor</td>
        <td class="column-3">梧槽</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-184 even">
        <td class="column-1">SE2</td>
        <td class="column-2">Rumbia</td>
        <td class="column-3">棕美</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-185 odd">
        <td class="column-1">PW1</td>
        <td class="column-2">Sam Kee</td>
        <td class="column-3">三记</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-186 even">
        <td class="column-1">PW4</td>
        <td class="column-2">Samudera</td>
        <td class="column-3">山姆</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-187 odd">
        <td class="column-1">BP11</td>
        <td class="column-2">Segar</td>
        <td class="column-3">实加</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-188 even">
        <td class="column-1">NS11</td>
        <td class="column-2">Sembawang</td>
        <td class="column-3">三巴旺</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-189 odd">
        <td class="column-1">STC</td>
        <td class="column-2">Sengkang</td>
        <td class="column-3">盛港</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-190 even">
        <td class="column-1">NE16</td>
        <td class="column-2">Sengkang</td>
        <td class="column-3">盛港</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-191 odd">
        <td class="column-1">BP13</td>
        <td class="column-2">Senja</td>
        <td class="column-3">信佳</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-192 even">
        <td class="column-1">NE12</td>
        <td class="column-2">Serangoon</td>
        <td class="column-3">实龙岗</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-193 odd">
        <td class="column-1">CC13</td>
        <td class="column-2">Serangoon</td>
        <td class="column-3">实龙岗</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-194 even">
        <td class="column-1">CR9</td>
        <td class="column-2">Serangoon North</td>
        <td class="column-3">实龙岗北</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-195 odd">
        <td class="column-1">TE19</td>
        <td class="column-2">Shenton Way</td>
        <td class="column-3">珊顿道</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-196 even">
        <td class="column-1">TE28</td>
        <td class="column-2">Siglap</td>
        <td class="column-3">实乞纳</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-197 odd">
        <td class="column-1">EW3</td>
        <td class="column-2">Simei</td>
        <td class="column-3">四美</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-198 even">
        <td class="column-1">DT7</td>
        <td class="column-2">Sixth Avenue</td>
        <td class="column-3">第六道</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-199 odd">
        <td class="column-1">NS23</td>
        <td class="column-2">Somerset</td>
        <td class="column-3">索美塞</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-200 even">
        <td class="column-1">PW7</td>
        <td class="column-2">Soo Teck</td>
        <td class="column-3">树德</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-201 odd">
        <td class="column-1">BP2</td>
        <td class="column-2">South View</td>
        <td class="column-3">南山</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-202 even">
        <td class="column-1">TE4</td>
        <td class="column-2">Springleaf</td>
        <td class="column-3">春叶</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-203 odd">
        <td class="column-1">CC6</td>
        <td class="column-2">Stadium</td>
        <td class="column-3">体育场</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-204 even">
        <td class="column-1">DT10</td>
        <td class="column-2">Stevens</td>
        <td class="column-3">史蒂芬</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-205 odd">
        <td class="column-1">TE11</td>
        <td class="column-2">Stevens</td>
        <td class="column-3">史蒂芬</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-206 even">
        <td class="column-1">PW6</td>
        <td class="column-2">Sumang</td>
        <td class="column-3">苏芒</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-207 odd">
        <td class="column-1">TE31</td>
        <td class="column-2">Sungei Bedok</td>
        <td class="column-3">双溪勿洛</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-208 even">
        <td class="column-1">CC11</td>
        <td class="column-2">Tai Seng</td>
        <td class="column-3">大成</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-209 odd">
        <td class="column-1">EW2</td>
        <td class="column-2">Tampines</td>
        <td class="column-3">淡滨尼</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-210 even">
        <td class="column-1">DT32</td>
        <td class="column-2">Tampines</td>
        <td class="column-3">淡滨尼</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-211 odd">
        <td class="column-1">DT33</td>
        <td class="column-2">Tampines East</td>
        <td class="column-3">淡滨尼东</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-212 even">
        <td class="column-1">CR6</td>
        <td class="column-2">Tampines North</td>
        <td class="column-3">淡滨尼北</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-213 odd">
        <td class="column-1">DT31</td>
        <td class="column-2">Tampines West</td>
        <td class="column-3">淡滨尼西</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-214 even">
        <td class="column-1">DT8</td>
        <td class="column-2">Tan Kah Kee</td>
        <td class="column-3">陈嘉庚</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-215 odd">
        <td class="column-1">EW4</td>
        <td class="column-2">Tanah Merah</td>
        <td class="column-3">丹那美拉</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-216 even">
        <td class="column-1">TE25</td>
        <td class="column-2">Tanjong Katong</td>
        <td class="column-3">丹戎加东</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-217 odd">
        <td class="column-1">EW15</td>
        <td class="column-2">Tanjong Pagar</td>
        <td class="column-3">丹戎巴葛</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-218 even">
        <td class="column-1">TE23</td>
        <td class="column-2">Tanjong Rhu</td>
        <td class="column-3">丹戎禺</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-219 odd">
        <td class="column-1">CR10</td>
        <td class="column-2">Tavistock</td>
        <td class="column-3">达维士笃</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-220 even">
        <td class="column-1">JW2</td>
        <td class="column-2">Tawas</td>
        <td class="column-3">大华士</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-221 odd">
        <td class="column-1">CR12</td>
        <td class="column-2">Teck Ghee</td>
        <td class="column-3">德义</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-222 even">
        <td class="column-1">PW2</td>
        <td class="column-2">Teck Lee</td>
        <td class="column-3">德利</td>
        <td class="column-4">Punggol LRT</td>
        <td class="column-5">榜鹅轻轨线</td>
    </tr>
    <tr class="row-223 odd">
        <td class="column-1">BP4</td>
        <td class="column-2">Teck Whye</td>
        <td class="column-3">德惠</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-224 even">
        <td class="column-1">DT18</td>
        <td class="column-2">Telok Ayer</td>
        <td class="column-3">直落亚逸</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-225 odd">
        <td class="column-1">CC28</td>
        <td class="column-2">Telok Blangah</td>
        <td class="column-3">直落布兰雅</td>
        <td class="column-4">Circle Line</td>
        <td class="column-5">环线</td>
    </tr>
    <tr class="row-226 even">
        <td class="column-1">BP14</td>
        <td class="column-2">Ten Mile Junction</td>
        <td class="column-3">十里广场</td>
        <td class="column-4">Bukit Panjang LRT</td>
        <td class="column-5">武吉班让轻轨线</td>
    </tr>
    <tr class="row-227 odd">
        <td class="column-1">JS3</td>
        <td class="column-2">Tengah</td>
        <td class="column-3">登加</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-228 even">
        <td class="column-1">JE2</td>
        <td class="column-2">Tengah Park</td>
        <td class="column-3">登加公园</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-229 odd">
        <td class="column-1">JE1</td>
        <td class="column-2">Tengah Plantation</td>
        <td class="column-3">登加种植</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-230 even">
        <td class="column-1">SW4</td>
        <td class="column-2">Thanggam</td>
        <td class="column-3">丹甘</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-231 odd">
        <td class="column-1">EW17</td>
        <td class="column-2">Tiong Bahru</td>
        <td class="column-3">中峇鲁</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-232 even">
        <td class="column-1">NS19</td>
        <td class="column-2">Toa Payoh</td>
        <td class="column-3">大巴窑</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-233 odd">
        <td class="column-1">JE4</td>
        <td class="column-2">Toh Guan</td>
        <td class="column-3">卓源</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-234 even">
        <td class="column-1">SW7</td>
        <td class="column-2">Tongkang</td>
        <td class="column-3">同港</td>
        <td class="column-4">Sengkang LRT</td>
        <td class="column-5">盛港轻轨线</td>
    </tr>
    <tr class="row-235 odd">
        <td class="column-1">EW31</td>
        <td class="column-2">Tuas Crescent</td>
        <td class="column-3">大士弯站</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-236 even">
        <td class="column-1">EW33</td>
        <td class="column-2">Tuas Link</td>
        <td class="column-3">大士连路站</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-237 odd">
        <td class="column-1">EW32</td>
        <td class="column-2">Tuas West Road</td>
        <td class="column-3">大士西路站</td>
        <td class="column-4">East West Line</td>
        <td class="column-5">东西线</td>
    </tr>
    <tr class="row-238 even">
        <td class="column-1">JS10</td>
        <td class="column-2">Tukang</td>
        <td class="column-3">都康</td>
        <td class="column-4">Jurong Region Line</td>
        <td class="column-5">裕廊区域线</td>
    </tr>
    <tr class="row-239 odd">
        <td class="column-1">CR14</td>
        <td class="column-2">Turf City</td>
        <td class="column-3">马城</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-240 even">
        <td class="column-1">DT27</td>
        <td class="column-2">Ubi</td>
        <td class="column-3">乌美</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-241 odd">
        <td class="column-1">DT34</td>
        <td class="column-2">Upper Changi</td>
        <td class="column-3">樟宜上段</td>
        <td class="column-4">Downtown Line</td>
        <td class="column-5">滨海市区线</td>
    </tr>
    <tr class="row-242 even">
        <td class="column-1">TE8</td>
        <td class="column-2">Upper Thomson</td>
        <td class="column-3">汤申路上段</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-243 odd">
        <td class="column-1">CR18</td>
        <td class="column-2">West Coast</td>
        <td class="column-3">西海岸</td>
        <td class="column-4">Cross Island Line</td>
        <td class="column-5">跨岛地铁线</td>
    </tr>
    <tr class="row-244 even">
        <td class="column-1">NS9</td>
        <td class="column-2">Woodlands</td>
        <td class="column-3">兀兰</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-245 odd">
        <td class="column-1">TE2</td>
        <td class="column-2">Woodlands</td>
        <td class="column-3">兀兰</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-246 even">
        <td class="column-1">TE1</td>
        <td class="column-2">Woodlands North</td>
        <td class="column-3">兀兰北</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-247 odd">
        <td class="column-1">TE3</td>
        <td class="column-2">Woodlands South</td>
        <td class="column-3">兀兰南</td>
        <td class="column-4">Thomson-East Coast Line</td>
        <td class="column-5">汤申-东海岸地铁线</td>
    </tr>
    <tr class="row-248 even">
        <td class="column-1">NE11</td>
        <td class="column-2">Woodleigh</td>
        <td class="column-3">兀里</td>
        <td class="column-4">North East Line</td>
        <td class="column-5">东北线</td>
    </tr>
    <tr class="row-249 odd">
        <td class="column-1">NS5</td>
        <td class="column-2">Yew Tee</td>
        <td class="column-3">油池</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-250 even">
        <td class="column-1">NS15</td>
        <td class="column-2">Yio Chu Kang</td>
        <td class="column-3">杨厝港</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
    <tr class="row-251 odd">
        <td class="column-1">NS13</td>
        <td class="column-2">Yishun</td>
        <td class="column-3">义顺</td>
        <td class="column-4">North South Line</td>
        <td class="column-5">南北线</td>
    </tr>
</tbody>"""
if __name__ == "__main__":
    soup = BeautifulSoup(table_html)
    rows = soup.find_all("tr")
    stations = [["StationCode", "StationName",
                 "StationNameChinese", "MRTLine", "MRTLineChinese"]]
    for row in rows:
        items = row.find_all("td")
        stations.append([item.text for item in items])
    with open("station_names.csv", "w") as file:
        csv_writer = writer(file, stations, delimiter=",")
        csv_writer.writerows(stations)
