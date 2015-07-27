<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/img/favicon.ico" type="image/x-icon" />
    <link rel="shortcut icon" href="/img/favicon.ico" type="image/x-icon" />

    <title>Your Cart - MongoMart</title>

    <!-- Bootstrap Core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="/static/css/shop-homepage.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
    <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>

<body>

% # Include navigation
%include('includes/nav.tpl')

<!-- Page Content -->
<div class="container">

    <div class="row">
        <div class="col-md-12">
            <ol class="breadcrumb">
                <li><a href="/">Home</a></li>
                <li class="active">Cart</li>
            </ol>
        </div>
    </div>

    %if updated == True:
        <p class="bg-warning" style="padding: 15px; font-size: 14px;">
            Your cart has been successfully updated.
        </p>
    %end

    <div class="row">
        <div class="col-md-12">
            <table class="table table-bordered table-striped">
                <thead>
                <tr>
                    <th>Product Name</th>
                    <th>Image</th>
                    <th>Quantity</th>
                    <th>Unit Price</th>
                    <th>Total</th>
                </tr>
                </thead>
                <tbody>

                % for item in cart['items']:
                <tr>
                    <form action="/cart/update">
                        <input type="hidden" name="itemid" value="{{item['_id']}}" />

                        <td><a href="/item?id={{item['_id']}}">{{item['title']}}</a></td>
                        <td class="muted center_text"><a href="/item?id={{item['_id']}}"><img width="300" src="/static/{{item['img_url']}}"></a></td>
                        <td>
                            <select name="quantity" onchange="this.form.submit()">
                                <option value="0">0 (Remove)</option>
                                %for i in range(1,26):
                                    %if item['quantity'] == i:
                                        <option value="{{i}}" selected>{{i}}</option>
                                    %else:
                                        <option value="{{i}}">{{i}}</option>
                                    %end
                                %end
                            </select>
                        </td>
                        <td>
                            {{"%0.2f" % item['price']}}
                        </td>
                        <td>
                            {{("%0.2f" % float(item['price'] * item['quantity']))}}
                        </td>

                    </form>
                </tr>
                %end

                <tr>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td><strong>{{"%0.2f" % total}}</strong></td>
                </tr>
                </tbody>
            </table>

        </div>



        <div class="row">
            <div class="col-md-12" style="text-align:right; padding-right: 30px;">
                <button class="btn btn-success" type="submit">Proceed to Checkout</button>
            </div>
        </div>
    </div>



</div>
<!-- /.container -->

% # Include footer
%include('includes/footer.tpl')

</body>

</html>
