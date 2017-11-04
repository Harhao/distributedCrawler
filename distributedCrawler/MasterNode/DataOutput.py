__author__ = 'Administrator'
import codecs
import time
class DataOutput(object):
    def __init__(self):
        self.filepath="baike_%s.html"%(time.strftime("%Y_%m_%d_%H_%S",time.localtime()))
        self.output_head(self.filepath)
        self.datas=[]
    def store_data(self,data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas):
            self.output_html(self.filepath)
    def output_head(self,path):
    # 将HTML头写进
        fout=codecs.open(path,'w',encoding='utf-8')
        fout.write("<html><body><table>")
        fout.close()
    def output_html(self,path):
        fout=codecs.open(path,'a',encoding='utf-8')
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>"%data['url'])
            fout.write("<td>%s</td>"%data['title'])
            fout.write("<td>%s</td>"%data['summary'])
            fout.write("</tr>")
            self.datas.remove(data)
        fout.close()
    def output(self,path):
        fout=codecs.open(path,'a',encoding='utf-8')
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

