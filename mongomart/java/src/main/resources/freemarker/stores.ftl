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

    <title>MongoMart - Locations</title>

    <!-- Bootstrap Core CSS -->
    <link href="/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="/css/shop-homepage.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
    <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

<#-- Include navigation -->
<#include "includes/nav.ftl">

<!-- Page Content -->
<div class="container">

    <div class="row">
        <div class="col-md-12">
            <ol class="breadcrumb">
                <li><a href="/">Home</a></li>
                <li>Locations</li>
            </ol>
        </div>
    </div>
    <!-- /.row -->

    <div class="row">


        <div class="col-md-12">
            <div class="row">
                <h2>Store Locator</h2>
                <p>Find the store closest to you.</p>
                <form class="form-horizontal">
                  <div class="form-group">
                    <label for="zipCode">Zip code</label>
                    <input type="text" class="form-control" name="zipCode" id="zipCode"/>
                  </div>
                  <div class="form-group">
                    <label> - or - </label>
                  </div>
                  <div class="form-group">
                    <label for="state">State</label>
                    <select class="form-control" name="state" id="state">
                      <#list states as state>
                      <option value="${state}">${state}</option>
                      </#list>
                    </select>
                  </div>
                  <div class="form-group">
                    <label for="city">City</label>
                    <input type="text" class="form-control" name="city" id="city">
                  </div>
                  <div class="form-group">
                    <button type="submit" class="btn btn-primary">Find stores</button>
                  </div>
                </form>
            </div>
            <!-- /.row -->

            <hr>


            <!-- Pagination -->
            <div class="row text-center">
                <div class="col-lg-12">
                    <ul class="pagination">
                    <#list 0..numPages as i>
                        <li <#if page == (i)>class="active"</#if>>
                            <a href="/search?page=${i}&query=">${i+1}</a>
                        </li>
                    </#list>
                    </ul>
                </div>
            </div>

            <div style="text-align:center;">
                <i>${numStores} Stores</i>
            </div>

            <!-- /.row -->
        </div>



    </div>

</div>
<!-- /.container -->

<#-- Include footer -->
<#include "includes/footer.ftl">

</body>

</html>
