#coding=UTF8
import sys

MENU_CATEGORY_LIST = [
    {'id':'mypage',
     'disp_name':'MyPage',
     'url':'/common/mypage',
     'is_link':'true',
    },
    {'id':'project',
     'disp_name':'Project情報',
     'url':'#project',
     'is_link':'false',
     'menu_list':[
         {'disp_name':'Project登録',
          'url':'/app/project/add'
         },
         {'disp_name':'Project修正',
          'url':'/app/project/search'
         },
     ]
    },
    {'id':'dp_use',
     'disp_name':'DP',
     'url':'#dp_use',
     'is_link':'false',
     'menu_list':[
         {'disp_name':'DP利用登録',
          'url':'/app/dp_use/add'
         },
         {'disp_name':'DP利用検索',
          'url':'/app/dp_use/search'
         },
     ]
    },

    {'id':'ab',
     'disp_name':'帳簿情報',
     'url':'#ab',
     'is_link':'false',
     'menu_list':[
         {'disp_name':'入金情報登録',
          'url':'/app/ab_d/add'
         },
         {'disp_name':'出金情報登録',
          'url':'/app/ab_w/add'
         },
         {'disp_name':'帳簿修正',
          'url':'/app/ab/search'
         },
     ]
    },
    {'id':'ab_plan',
     'disp_name':'予定情報',
     'url':'#ab_plan',
     'is_link':'false',
     'menu_list':[
         {'disp_name':'入金予定登録',
          'url':'/app/ab_plan_d/add'
         },
         {'disp_name':'出金予定登録',
          'url':'/app/ab_plan_w/add'
         },
         {'disp_name':'予定修正',
          'url':'/app/ab_plan/search'
         },
     ]
    },
    {'id':'ab_sum',
     'disp_name':'帳簿集計',
     'url':'#ab_sum',
     'is_link':'false',
     'menu_list':[
         {'disp_name':'帳簿集計(日別)',
          'url':'/app/ab/sum'
         },
         {'disp_name':'帳簿集計(月別)',
          'url':'/app/ab/sum_by_month'
         },
         {'disp_name':'帳簿集計(年度別)',
          'url':'/app/ab/sum_by_year'
         },
         {'disp_name':'帳簿集計(Project別)',
          'url':'/app/ab/sum_by_project'
         },
     ]
    },
    {'id':'bab',
     'disp_name':'残高照会',
     'url':'#bab',
     'is_link':'false',
     'menu_list':[
         {'disp_name':'口座残高照会',
          'url':'/app/bab/inquiry'
         },
     ]
    },
    {'id':'mst',
     'disp_name':'マスタ保守',
     'url':'#mst',
     'is_link':'false',
     'menu_list':[
         {'disp_name':'勘定科目登録',
          'url':'/app/at/add'
         },
         {'disp_name':'勘定科目修正',
          'url':'/app/at/search'
         },
         {'disp_name':'銀行口座登録',
          'url':'/app/ba/add'
         },
         {'disp_name':'銀行口座修正',
          'url':'/app/ba/search'
         },
         {'disp_name':'支出収入方法登録',
          'url':'/app/dwm/add'
         },
         {'disp_name':'支出収入方法修正',
          'url':'/app/dwm/search'
         },
         {'disp_name':'汎用パラメーター登録',
          'url':'/app/gp/add'
         },
         {'disp_name':'汎用パラメーター修正',
          'url':'/app/gp/search'
         },
         {'disp_name':'データパターン登録',
          'url':'/app/dp/add'
         },
         {'disp_name':'データパターン修正',
          'url':'/app/dp/search'
         },
     ]
    },
    {'id':'setting',
     'disp_name':'設定',
     'url':'#setting',
     'is_link':'false',
     'menu_list':[
         {'disp_name':'パスワード変更',
          'url':'/common/password/edit'
         },
         {'disp_name':'ログアウト',
          'url':'/common/logout'
         },
     ]
    },
]