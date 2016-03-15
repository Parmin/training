#include <iostream>
#include <mongocxx/client.hpp>
#include <mongocxx/cursor.hpp>
#include <mongocxx/collection.hpp>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/builder/basic/kvp.hpp>
#include <mongocxx/exception/exception.hpp>
#include <mongocxx/exception/operation_exception.hpp>
#include <mongocxx/insert_many_builder.hpp>
#include <bsoncxx/json.hpp>

using namespace bsoncxx::builder::stream;
using namespace mongocxx;

//using namespace bsoncxx::builder::basic;

void insert(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["simple"];
  //create a document
  auto doc0 = document{} << "name" << "Dwight" << finalize;

  //insert the document
  auto result = coll.insert_one(doc0.view());
}

void insert_with_id(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["set__id"];

  //create a document
  auto doc1 = document{} << "_id" << 1 << "name" << "Dwight" << finalize;

  //insert the document
  coll.insert_one(doc1.view());
  //
  auto cursor = coll.find({});
  for (auto&& x : cursor) {
    std::cout << "_id: " << x["_id"].get_int32() << std::endl;
  }
}


void insert__id_array(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["_id_array"];

  int a[3] = {0,1,2};
  //initialize a document
  auto doc2 = document{} << "_id" << open_array << 0 << 1 << 2<< close_array<< finalize;

  //insert a document
  coll.insert_one(doc2.view());

}

void insert_malformed(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["malformed"];

  //initialize a document
  //auto doc4 = document{} << hello" << finalize;

  //insert a document
  //coll.insert_one(doc4.view());


}


void insert_many_ordered(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["ordered"];
  //instantiate vector of document views!
  std::vector<bsoncxx::document::view> docs{};

  auto b0 = document{} << "_id" << 0 << "name" << "Soccer" << finalize;
  auto b1 = document{} << "_id" << 1 << "name" << "Rugby" << finalize;
  auto b2 = document{} << "_id" << 0 << "name" << "Tennis" << finalize;
  auto b3 = document{} << "_id" << 2 << "name" << "Football" << finalize;


  docs.push_back(b0.view());
  docs.push_back(b1.view());
  docs.push_back(b2.view());
  docs.push_back(b3.view());


  //insert ordered (default)
  try{
    coll.insert_many(docs, options::insert{});
  } catch ( const operation_exception &ex ) {
    std::cout << "caught op exception -> " << bsoncxx::to_json(ex.raw_server_error()->view()) << std::endl;
  }
}

void insert_many_unordered(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["unordered"];
  //instantiate vector of document views!
  std::vector<bsoncxx::document::view> docs{};

  auto b0 = document{} << "_id" << 0 << "name" << "Badminton" << finalize;
  auto b1 = document{} << "_id" << 1 << "name" << "Snooker" << finalize;
  auto b2 = document{} << "_id" << 0 << "name" << "Karts" << finalize;
  auto b3 = document{} << "_id" << 2 << "name" << "Javellin throw" << finalize;

  docs.push_back(b0.view());
  docs.push_back(b1.view());
  docs.push_back(b2.view());
  docs.push_back(b3.view());

  //insert unordered
  auto options = options::insert{};
  options.ordered(false);
  try{
    coll.insert_many(docs, options);
  } catch ( const operation_exception &ex ) {
    std::cout << "caught op exception -> " << bsoncxx::to_json(ex.raw_server_error()->view()) << std::endl;
  }
}

void delete_after_find(){

  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["stuff"];


  auto cursor = coll.find({});
  document delete_query;
  for ( auto&& x : cursor){
    delete_query << "_id" << x["_id"].get_oid();
    auto result = coll.delete_one(delete_query.view());
    std::cout << "Result:  " << result->deleted_count() << std::endl;
  }

}


void drop_collection(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["names"];

  auto b0 = document{} << "_id" << 0 << "name" << "Meghan" << finalize;
  auto b1 = document{} << "_id" << 1 << "name" << "Elizabeth" << finalize;
  auto b2 = document{} << "_id" << 2 << "name" << "Beatriz" << finalize;
  auto b3 = document{} << "_id" << 3 << "name" << "Anna" << finalize;


  coll.drop();
}

void drop_database(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate database object
  database db = conn["tempDB"];
  //instantiate collections
  collection coll1 = db["coll1"];
  collection coll2 = db["coll2"];
  // insert one document on first collection
  auto b1 = document{} << "brand" << "Mercedes Benz" << finalize;
  auto result1 = coll1.insert_one(b1.view());
  std::cout << "Inserted " << bsoncxx::to_json(result1->inserted_id()) << std::endl;
  // insert one document on second collection
  auto b2 = document{} << "drink" << "Gin Tonic" << finalize;
  auto result2 = coll2.insert_one(b2.view());
  std::cout << "Inserted " << bsoncxx::to_json(result2->inserted_id()) << std::endl;

  // list all collections
  auto cursor = db.list_collections();

  auto count = std::distance(cursor.begin(), cursor.end());
  std::cout << "Number of collections: " << count << std::endl;


  db.drop();

  cursor = db.list_collections();
  count = std::distance(cursor.begin(), cursor.end());
  std::cout << "Number of collections: " << count << std::endl;
}

void insert_many(bool ordered){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["unordered"];
  //instantiate vector of document views!
  std::vector<bsoncxx::document::view> docs{};

  auto b0 = document{} << "_id" << 0 << "name" << "Badminton" << finalize;
  auto b1 = document{} << "_id" << 1 << "name" << "Snooker" << finalize;
  auto b2 = document{} << "_id" << 0 << "name" << "Karts" << finalize;
  auto b3 = document{} << "_id" << 2 << "name" << "Javellin throw" << finalize;

  docs.push_back(b0.view());
  docs.push_back(b1.view());
  docs.push_back(b2.view());
  docs.push_back(b3.view());

  //insert unordered
  auto options = options::insert{};
  options.ordered(ordered);
  try{
    coll.insert_many(docs, options);
  } catch ( const operation_exception &ex ) {
    std::cout << "caught op exception -> " << bsoncxx::to_json(ex.raw_server_error()->view()) << std::endl;
  }
}



int main(int, char**) {
    try{
      insert_many(false);
    } catch( const exception &e ) {
      std::cout << "caught " << e.what() << std::endl;
    }
    return EXIT_SUCCESS;

}
