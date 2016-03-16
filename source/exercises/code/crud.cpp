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

void insert_many(collection& coll, bool ordered){
  //instantiate vector of document views!
  std::vector<bsoncxx::document::view> docs{};

  auto b0 = document{} << "_id" << 0 << "name" << "Badminton" << "indoor" << true << finalize;
  auto b1 = document{} << "_id" << 1 << "name" << "Snooker" << "indoor" << true << finalize;
  auto b2 = document{} << "_id" << 0 << "name" << "Karts" << "indoor" << false << finalize;
  auto b3 = document{} << "_id" << 2 << "name" << "Javellin throw" << "indoor" << true << finalize;

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



void read_simple(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["sports"];
  coll.drop();
  insert_many(coll, false);
  // returns all documents in collection
  auto cursor = coll.find({});
  for( auto&& d : cursor){
    std::cout << bsoncxx::to_json(d) << std::endl;
  }
  auto query = document{} << "_id" << 0 << finalize;
  // returns one document that has _id = 0
  std::cout << "query << \"_id\" << 0;" << std::endl;
  for ( auto&& d : coll.find(query.view())){
    std::cout << bsoncxx::to_json(d) << std::endl;
  }

  auto query2 = document{} << "name" << "Snooker" << "indoor" << true << finalize;
  std::cout << "query" << bsoncxx::to_json(query2.view()) << std::endl;

  for ( auto&& d : coll.find(query2.view())){
    std::cout << bsoncxx::to_json(d) << std::endl;
  }

}


void insert_sports(collection &coll){
  coll.drop();
  auto b0 = document{} << "name" << "Badminton"
      << "category" << open_array
        << "field" << "indoor" << "pairs" << "individual" << close_array
      << finalize;
  auto b1 = document{} << "name" << "Javelin throw"
      << "category" << open_array
        << "individual" << "track" << "outdoors" << close_array
      << finalize;
  auto b2 = document{} << "name" << "Football (not soccer!)"
      << "category" << open_array
        << "team" << "field" << "outdoors" << close_array
      << finalize;
  std::vector<bsoncxx::document::view> docs{};
  docs.push_back(b0.view());
  docs.push_back(b1.view());
  docs.push_back(b2.view());
  auto options = options::insert{};
  options.ordered(true);
  coll.insert_many(docs, options );
}

void iterate_cursor(cursor c, std::string name ){
  std::cout << name << std::endl;
  for ( auto&& d : c ){
    std::cout << bsoncxx::to_json(d) << std::endl;
  }
}

void find_array(){
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["sports"];
  insert_sports(coll);

  // Match documents where "category" contains the value specified
  auto query0 = document{} << "category" << "field" << finalize;
  // Should return 2 documents
  iterate_cursor(coll.find(query0.view()), "query0");


  // Match documents where "category" equals the value specified
  auto query1 = document{} << "category" << open_array
    << "team" << close_array
  << finalize;
  // no documents
  iterate_cursor(coll.find(query1.view()), "query1");

  // only the second document
  auto query2 = document{} << "category" << open_array
    << "individual" << "track" << "outdoors" << close_array
  << finalize;
  iterate_cursor(coll.find(query2.view()), "query2");
}

void find_subdocument(collection &coll){

  // find worldcup is {teams : 32}
  auto query0 = document{} << "worldcup"<< open_document
      << "teams" << 32
    << close_document
  << finalize;
  iterate_cursor(coll.find(query0.view()), "query0");


  auto query1 = document{} << "worldcup.teams" << 32 << finalize;
  iterate_cursor(coll.find(query1.view()), "query1");
}

void insert_subdocument(){
  client conn{mongocxx::uri{}};
  collection coll = conn["sample"]["sports"];
  coll.drop();
  auto b0 = document{} << "name" << "Football (not soccer!)"
      << "worldcup" << open_document
        << "host" << "Brazil"
        << "teams" << 32
        << "champion" << "Germany"
      << close_document
    << finalize;
  auto b1 = document{} << "name" << "Rugby"
      << "worldcup" << open_document
        << "host" << "England"
        << "teams" << 20
        << "champion" << "New Zeland"
      << close_document
    << finalize;
  coll.insert_one(b0.view());
  coll.insert_one(b1.view());
  find_subdocument(coll);
}


void find_projected(collection &coll){
  document query;
  document projection;

  query << "title" << "Forrest Gump";
  projection <<  "title" << 1 << "imdb_rating" << 1;
  options::find opts;
  opts.projection( projection.view());
  iterate_cursor(coll.find(query.view(), opts), "queryprojected");

}

void find_movies(){
  client conn{mongocxx::uri{}};
  collection coll = conn["sample"]["movies"];

  find_projected(coll);
}

void insert_loop(){
  client conn{mongocxx::uri{}};
  collection coll = conn["sample"]["iterate"];
  coll.drop();
  for (int i=1; i<=10000; i++) {
      document b0;
      b0 << "a" << i;
      coll.insert_one(b0.view());
  }

  cursor c = coll.find({});

  for ( auto&& d : c ){
    std::cout << bsoncxx::to_json(d) << std::endl;
  }
}

void find_distinct(){
  client conn{mongocxx::uri{}};
  collection coll = conn["sample"]["distinct"];
  coll.drop();
}


int main(int, char**) {
    try{
      insert_loop();
    } catch( const exception &e ) {
      std::cout << "caught " << e.what() << std::endl;
    }
    return EXIT_SUCCESS;

}
