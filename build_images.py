#!/usr/bin/env python


from os import getcwd, chdir, system
import glob
chdir(getcwd())
file_list = glob.glob("*.jpg") + glob.glob("*.png")
for file in file_list:
    print "Generating eps for", file
    just_name = file.split(".")[0]
    system("convert {0} eps3:{1}.eps".format(file, just_name))
    print "Generating rst for", file
    f = open("{0}.rst".format(just_name), "w+")
    f.write(
        """
    
        .. only:: latex and not offset
    
           .. figure:: /images/{0}
              :alt: TODO - add desc
              :align: center
              :figwidth: 1600px
    
        .. only:: website and slides
    
           .. figure:: /images/{0}
              :alt: TODO - add desc
              :align: center
              :figwidth: 700px
    
        .. only:: website and html
    
           .. figure:: /images/{0}
              :alt: TODO - add desc
              :align: center
              :figwidth: 700px
    
        .. only:: website and not (html or slides)
    
           .. raw:: html
    
              <div class="figure align-center" style="max-width:700px;"><img src="http://docs.mongodb.org/training/master/_images/{0}" alt="Description"></img><p>Description</p></div>
    
        .. only:: latex and offset
    
           .. raw:: latex
    
              \\begin{{figure}}[h!]
                \\centering
                \\includegraphics[width=400px]{{{1}.eps}}
              \\end{{figure}}
    
        """.format(file, just_name)
    )
    f.close()


