class Pagination:
    def __init__(self,page_num,total_data_num,per_page=15,max_show=11):
        try:
            self.page_num = int(page_num)
            if self.page_num <= 0:
                self.page_num = 1
        except Exception as e:
            self.page_num = 1
        self.total_data_num = total_data_num  # 总数据条数
        self.per_page = per_page  # 每页显示条数
        self.total_page_num, more = divmod(total_data_num, per_page)
        if more:
            self.total_page_num += 1
        self.max_show = max_show
        self.half_show = self.max_show // 2
    @property
    def start(self):
        return (self.page_num-1) * self.per_page
    @property
    def end(self):
        return self.page_num * self.per_page
    @property
    def page_html(self):
        page_start = self.page_num - self.half_show
        page_end = self.page_num + self.half_show
        if self.total_page_num >= self.max_show:
            if page_start <= 0:
                page_start = 1
                page_end = self.max_show
            elif page_end > self.total_page_num:
                page_start = self.total_page_num - self.max_show + 1
                page_end = self.total_page_num
        else:
            page_start = 1
            page_end = self.total_page_num

        # 上下翻页和点击的页面效果
        page_list = []
        if self.page_num == 1:
            page_list.append('<li class="disabled"><a >上一页</a></li>')
        else:
            page_list.append('<li><a href="?page={}">上一页</a></li>'.format(self.page_num - 1))
        for i in range(page_start, page_end + 1):
            if i == self.page_num:
                page_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
            else:
                page_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))
        if self.page_num == self.total_page_num:
            page_list.append('<li class="disabled"><a>下一页</a></li>')
        else:
            page_list.append('<li><a href="?page={}">下一页</a></li>'.format(self.page_num + 1))
        return ''.join(page_list)
