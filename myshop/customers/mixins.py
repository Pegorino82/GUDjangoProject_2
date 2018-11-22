from django.shortcuts import redirect

class AdminGroupRequired:
    redirect_url = ''

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(
            [
                'productsapp.add_product',
                'productsapp.change_product',
                'productsapp.delete_product',
                'categoriesapp.add_category',
                'categoriesapp.change_category',
                'categoriesapp.delete_category',
            ]
        ):
            return super(AdminGroupRequired, self).dispatch(request, *args, **kwargs)
        return redirect(self.redirect_url)
