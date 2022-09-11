import sys;
import re;
from texoutparse import LatexLogParser;

apply_filter = True;

# specify as keys the keys of the LatexLogParser output and as values a list with regex strings
# could be replaced by a json-file
warning_filter = {
                    "message" : [
                                 re.compile("(.*) float specifier changed to (.*)"),
                                 re.compile("(.*)may have changed. Rerun to get cross(.*)"),
                                 re.compile("(.*)run BibTeX on the file(.*)"),
                                ],
                    "component" : [ re.compile("Font") ],
                    "package" : [ re.compile("rerunfilecheck") ],
                              
                 };
error_filter = {
                "message" : [
                                 re.compile("Dimension too large")
                             ]
};

def caption(s, level=1):
  if level == 0:
    sf = "    "+s+"    ";
    print("="*len(sf));
    print(sf);
    print("="*len(sf));
  elif level == 1:
    print(s);
    print('-'*len(s))

def printitem(itm, desc, filter):
  nw = len(itm);
  if nw == 0:
    print("None found.");
    return 0;
  num_ignored = 0;
  for iw, w in enumerate(itm):
    w_info = w.info;
    
    ignore = False;
    for k,v in w_info.items():
      if k in filter:
        if filter[k] is not None:
          for reg in filter[k]:
            if reg.match(v) is not None:
              ignore=True;
    
    if ignore:
      num_ignored += 1; continue;
    
    w_type = ""
    if 'type' in w_info:
        w_type = w_info['type'];
    w_msg  = w_info['message'];
    w_additional_info = {k:v for k,v in w_info.items() if k not in ['type', 'message']};
    print("{d} {i}/{n} (Type {t})".format(d=desc, i=iw+1,n=nw,t=w_type));
    print(w_msg);
    add_info_strs = [ "{it}: {im}".format(it=k, im=v)
                      for k,v in w_additional_info.items() ];
    print("\n".join(add_info_strs));
    print("");
  return num_ignored;

def get_encoding(file_name):
    """
    Requires:
    pip install charset-normalizer
    """
    from charset_normalizer import detect
    return detect(open(file_name,'rb').read())["encoding"]

if __name__ == '__main__':
    log_file_path = sys.argv[1];
    if not apply_filter:
      warning_filter = {}
      error_filter = {};
    
    parser = LatexLogParser()
    with open(log_file_path, encoding=get_encoding(log_file_path)) as f:
        parser.process(f)
    
    caption(log_file_path, 0);
    print("")
    caption("Summary",1);
    print(parser)
    print("")
    caption("Warnings");
    iw = printitem(parser.warnings, "Warning", warning_filter);
    print(iw, " Warnings were ignored.");
    print("");
    caption("Errors");
    ie = printitem(parser.errors, "Error", error_filter);
    print(ie, " Errors were ignored.");
    print("");
