# file name from node-red 
# import sys
# stdIN_filename = sys.stdin.readline() # รับชื่อภาพมาเลย 
# # print(stdIN_filename)
# keep = stdIN_filename + ''
# print(keep)
# สั่งรัน ไฟล์ 
# import ipynb2py_for_exe_on_rasp_fix_roi_6_node
# execfile('ipynb2py_for_exe_on_rasp_fix_roi_6_node') old
# exec(open('ipynb2py_for_exe_on_rasp_fix_roi_6_node').read())
# พร้อมส่งค่า

def exec_full(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)

# Execute the file.
exec_full('D:/________mask_rcnn________2/find_area_pixel_leaf_/samples/leaf_script/ipynb2py_for_exe_on_rasp_fix_roi_6_node.py')