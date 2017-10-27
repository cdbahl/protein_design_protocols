#!/usr/bin/python
from pymol import cmd
import glob
import re


#load all pdb files in a directory
def load_sep(files,obj=''):
  """
  load_sep <files>, <object>

  loads multiple files (using filename globbing)
  into a multiple objects (e.g. from modelling or NMR).

  e.g. load_sep prot_*.pdb, prot
  """
  file_list = glob.glob(files)
  file_list.sort()
# find both directory prefixes and file type suffixes
  extension = re.compile( '(^.*[\/]|\.(pdb|ent|brk))' )

  if file_list:
    for i in range(len(file_list)):
      if ( obj == '' ):
        obj_name = extension.sub('',file_list[i])
      else:
        obj_name = "%s_%d" % (obj,i)

      cmd.load(file_list[i],obj_name)
  else:
    print "No files found for pattern %s" % files
    
cmd.extend('load_sep',load_sep)



#scroll through structures using page up and page down keys
def move_down():
	enabled_objs = cmd.get_names("objects",enabled_only=1)
	all_objs = cmd.get_names("objects",enabled_only=0)
	for obj in enabled_objs:
		cmd.disable(obj)
		last_obj=obj
		for i in range(0,len(all_objs)):
			if all_objs[i] == obj:
				if i+1 >= len(all_objs):
					cmd.enable( all_objs[0] )
				else:
					cmd.enable( all_objs[i+1] )
	cmd.orient
def move_up():
	enabled_objs = cmd.get_names("objects",enabled_only=1)
        all_objs = cmd.get_names("objects",enabled_only=0)
        for obj in enabled_objs:
                cmd.disable(obj)
                last_obj=obj
                for i in range(0,len(all_objs)):
                        if all_objs[i] == obj:
                                if i-1 < 0:
                                        cmd.enable( all_objs[-1] )
                                else:
                                        cmd.enable( all_objs[i-1] )
	cmd.orient
cmd.set_key('pgup', move_up)
cmd.set_key('pgdn', move_down)
#cmd.set_key('up', move_up)
#cmd.set_key('down', move_down)
#cmd.set_key('left', move_up)
#cmd.set_key('right', move_down)



#align all structures and display as cartoon with disulfide sticks with left and right arrow keys
def align_structure():
    all_objs = cmd.get_names("objects",enabled_only=0)
    for i in cmd.get_object_list(): 
        cmd.align( i, all_objs[0] )
        cmd.center( i ,animate=-1)

def gv():
    all_objs = cmd.get_names("objects",enabled_only=0)
    for i in cmd.get_object_list(): 
        cmd.hide("everything", i)
        cmd.show("cartoon", i)
        #cmd.show("surface", i)
        cmd.show("lines", i)
        if i <> 'peptide_on_target-keep':
            cmd.show("stick", "resname CYS and not name c+n+o")   
        cmd.hide("everything", "symbol H")     
    #cmd.set("surface_cavity_mode", 1)
    #cmd.set("surface_type",2)

cmd.set_key('right',gv)#hide_chain_b)
cmd.set_key('left',align_structure)
