# Classification (U)

"""Program:  rabbitmq_class.py

    Description:  Class definitions and methods for RabbitMQ system.

    Functions:
        pub_2_rmq
        create_rmqcon
        create_rmqpub

    Classes:
        RabbitMQ
            RabbitMQPub
                RabbitMQCon
        RabbitMQBase
            RabbitMQAdmin

"""

# Libraries and Global Variables
from __future__ import absolute_import

# Standard
import copy
import json
import pika
import requests
from six.moves import urllib

# Local
try:
    from . import version

except (ValueError, ImportError) as err:
    import version

__version__ = version.__version__

# Global
KEY1 = "pass"
KEY2 = "word"
KEY3 = "_hash"
API_VHOST = "/api/vhosts/{0}"
API_USER = "/api/users/{0}"
API_PERM = "/api/permissions/{0}/{1}"
API_QUEUE = "/api/queues/{0}/{1}"


def pub_2_rmq(cfg, data):

    """Function:  pub_2_rmq

    Description:  All in one function to publish to a RabbitMQ queue.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) data -> Data document.
        (output) status -> True|False - Success of publishing to RabbitMQ.
        (output) err_msg -> Error message, if any.

    """

    rmq = create_rmqpub(cfg, cfg.queue, cfg.r_key)
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        if rmq.publish_msg(data):
            status = True
            err_msg = None

        else:
            status = False
            err_msg = "Failure in publishing to RabbitMQ"

    else:
        status = False

    rmq.drop_connection()

    return status, err_msg


def create_rmqcon(cfg, q_name, r_key):

    """Function:  create_rmqcon

    Description:  Create a RabbitMQ Consumer instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) q_name -> Queue name in RabbitMQ.
        (input) r_key -> Routing key in RabbitMQ.
        (output) RabbitMQ Consumer instance.

    """

    heartbeat = cfg.heartbeat if hasattr(cfg, "heartbeat") else 60
    host_list = cfg.host_list if hasattr(cfg, "host_list") else list()
    no_ack = cfg.no_ack if hasattr(cfg, "no_ack") else False

    return RabbitMQCon(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=q_name, routing_key=r_key, x_durable=cfg.x_durable,
        q_durable=cfg.q_durable, auto_delete=cfg.auto_delete, no_ack=no_ack,
        heartbeat=heartbeat, host_list=host_list)


def create_rmqpub(cfg, q_name, r_key):

    """Function:  create_rmqpub

    Description:  Create a RabbitMQ Publisher instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) q_name -> Queue name in RabbitMQ.
        (input) r_key -> Routing key in RabbitMQ.
        (output) RabbitMQ Publisher instance.

    """

    heartbeat = cfg.heartbeat if hasattr(cfg, "heartbeat") else 60
    host_list = cfg.host_list if hasattr(cfg, "host_list") else list()

    return RabbitMQPub(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=q_name, routing_key=r_key, x_durable=cfg.x_durable,
        q_durable=cfg.q_durable, auto_delete=cfg.auto_delete,
        heartbeat=heartbeat, host_list=host_list)


class RabbitMQ(object):

    """Class:  RabbitMQ

    Description:  Class which is a representation of a RabbitMQ message
        system.  A RabbitMQ object is used as proxy to implement the
        connecting to and closing connection to a RabbitMQ node.

    Methods:
        __init__
        connect
        close

    """

    def __init__(self, user, japd, host="localhost", port=5672, **kwargs):

        """Method:  __init__

        Description:  Initialization of an instance of the RabbitMQ class.

        Arguments:
            (input) user -> User login name.
            (input) japd -> User psword.
            (input) host -> Hostname of RabbitMQ node.
            (input) port -> RabbitMQ port.  Default port is 5672.
            (input) kwargs:
                host_list -> List of RabbitMQ nodes in a cluster.
                heartbeat -> Time in seconds to keep connection alive.

        """

        self.name = user
        self.host = host
        self.port = port
        self.connection = None
        self.host_list = kwargs.get("host_list", list())
        self.heartbeat = kwargs.get("heartbeat", 60)
        self.creds = pika.PlainCredentials(self.name, japd)

        if self.host_list:
            self.params = list()

            for node in self.host_list:
                node_port = node.split(":")
                params = pika.ConnectionParameters(
                    host=node_port[0], port=int(node_port[1]),
                    credentials=self.creds, heartbeat=self.heartbeat)
                self.params.append(params)

        else:
            self.params = pika.ConnectionParameters(
                host=self.host, port=self.port, credentials=self.creds,
                heartbeat=self.heartbeat)

    def connect(self):

        """Method:  connect

        Description:  Connects the instance to a RabbitMQ node.

        Arguments:
            (output) connect_status -> True|False - Successfully connected.
            (output) err_msg -> Error message if unsuccessful connection.

        """

        err_msg = None
        connect_status = True

        try:
            self.connection = pika.BlockingConnection(self.params)

        except pika.exceptions.ConnectionClosed as msg:
            err_msg = msg
            connect_status = False

        except pika.exceptions.ProbableAuthenticationError as msg:
            err_msg = msg
            connect_status = False

        except Exception as msg:
            err_msg = msg
            connect_status = False

        return connect_status, err_msg

    def close(self):

        """Method:  close

        Description:  Close the connection to the RabbitMQ node.

        Arguments:

        """

        self.connection.close()


class RabbitMQPub(RabbitMQ):

    """Class:  RabbitMQPub

    Description:  Class which is a representation of a RabbitMQ Publisher, to
        include setting up a connection and channel, creating an exchange and
        queue and dropping and clearing these properties.  A RabbitMQPub object
        is used as proxy to implement the publishing a message to a RabbitMQ
        queue.

    Methods:
        __init__
        open_channel
        close_channel
        create_queue
        setup_exchange
        bind_queue
        publish_msg
        setup_queue
        create_connection
        drop_connection
        check_confirm
        drop_queue
        clear_queue
        unbind_queue
        drop_exchange

    """

    def __init__(self, user, japd, host="localhost", port=5672, **kwargs):

        """Method:  __init__

        Description:  Initialization of an instance of the RabbitMQPub class.

        Arguments:
            (input) user -> User login name.
            (input) japd -> User psword.
            (input) host -> Hostname of RabbitMQ node.
            (input) port -> RabbitMQ port.  Default = 5672.
            (input) kwargs:
                exchange_name -> Name of exchange.
                exchange_type -> Types: direct, fanout, headers, and topic.
                queue_name -> Name of the queue to create.
                routing_key -> Name of queue to rout to.
                x_durable -> True|False - Exchange survives reboots.
                q_durable -> True|False - Queue survives reboots.
                auto_delete -> True|False - Auto-delete after consuming.
                host_list -> List of RabbitMQ nodes in a cluster.
                heartbeat -> Time in seconds to keep connection alive.

        """

        super(RabbitMQPub, self).__init__(user, japd, host, port, **kwargs)

        self.channel = None

        # Queue declaration attributes
        self.queue_name = kwargs.get("queue_name", "")
        self.q_durable = kwargs.get("q_durable", True)
        self.auto_delete = kwargs.get("auto_delete", False)
        self.q_passive = False
        self.routing_key = kwargs.get("routing_key", "")

        # Exchange declaration attributes
        self.exchange = kwargs.get("exchange_name", "")
        self.exchange_type = kwargs.get("exchange_type", "direct")
        self.x_durable = kwargs.get("x_durable", True)
        self.x_passive = False

    def open_channel(self):

        """Method:  open_channel

        Description:  Open a channel to a RabbitMQ node.

        Arguments:

        """

        self.channel = self.connection.channel()

    def close_channel(self):

        """Method:  close_channel

        Description:  Close the channel to the RabbitMQ node.

        Arguments:

        """

        self.channel.close()

    def create_queue(self):

        """Method:  setup_queue

        Description:  Setup a queue on a RabbitMQ node.

        Arguments:

        """

        self.channel.queue_declare(queue=self.queue_name,
                                   durable=self.q_durable,
                                   auto_delete=self.auto_delete)

    def setup_exchange(self):

        """Method:  setup_exchange

        Description:  Create an exchange on a RabbitMQ node.

        Arguments:

        """

        self.channel.exchange_declare(
            exchange=self.exchange, exchange_type=self.exchange_type,
            durable=self.x_durable)

    def bind_queue(self):

        """Method:  bind_queue

        Description:  Bind a queue to an exchange.

        Arguments:

        """

        self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange,
                                routing_key=self.routing_key)

    def publish_msg(self, body, mandatory=True):

        """Method:  publish_msg

        Description:  Publish a message to a RabbitMQ queue.

        Arguments:
            (input) body -> Message body being published to RabbitMQ.
            (input) mandatory -> True|False - Message is saved to queue.
            (output) status -> True|False -> Message confirmation delivery.

        """

        if pika.__version__ < '1.0.0':
            status = self.channel.basic_publish(
                exchange=self.exchange, routing_key=self.routing_key,
                body=body, mandatory=mandatory,
                properties=pika.BasicProperties(delivery_mode=2))

        else:
            try:
                self.channel.basic_publish(
                    exchange=self.exchange, routing_key=self.routing_key,
                    body=body, mandatory=mandatory,
                    properties=pika.BasicProperties(delivery_mode=2))
                status = True

            except pika.exceptions.UnroutableError:
                status = False

        return status

    def setup_queue(self):

        """Method:  setup_queue

        Description:  Initialize the exchange and queue and bind the queue to
            the exchange.

        Arguments:

        """

        self.setup_exchange()
        self.create_queue()
        self.bind_queue()
        self.check_confirm()

    def create_connection(self):

        """Method:  create_connection

        Description:  Create a connection and a channel, followed by the
            initialization of an exchange and queue.

        Arguments:
            (output) connect_status -> True|False - Successfully connected.
            (output) err_msg -> Error message if unsuccessful.

        """

        connect_status, err_msg = self.connect()

        if connect_status:
            self.open_channel()

            if self.channel.is_open:
                self.setup_queue()

            else:
                connect_status = False
                err_msg = "Error:  Unable to open channel."

        return connect_status, err_msg

    def drop_connection(self):

        """Method:  drop_connection

        Description:  Drop the channel and connection to RabbitMQ.

        Arguments:

        """

        self.close_channel()
        self.close()

    def check_confirm(self):

        """Method:  check_confirm

        Description:  Turn on the check confirmation for the channel.

        Arguments:

        """

        self.channel.confirm_delivery()

    def drop_queue(self, if_unused=True, if_empty=True):

        """Method:  drop_queue

        Description:  Drop the queue from the exchange.

        Arguments:
            (input) if_unused -> True|False - Only drop if unused.
            (input) if_empty -> True|False - Only drop if empty.

        """

        self.channel.queue_delete(queue=self.queue_name, if_unused=if_unused,
                                  if_empty=if_empty)

    def clear_queue(self):

        """Method:  clear_queue

        Description:  Remove messages from queue.

        Arguments:

        """

        self.channel.queue_purge(queue=self.queue_name)

    def unbind_queue(self):

        """Method:  unbind_queue

        Description:  Unbind a queue from an exchange.

        Arguments:

        """

        self.channel.queue_unbind(
            queue=self.queue_name, exchange=self.exchange,
            routing_key=self.routing_key)

    def drop_exchange(self, if_unused=True):

        """Method:  drop_exchange

        Description:  Drop an exchange from the RabbitMQ node.

        Arguments:
            (input) if_unused -> True|False - Only drop if unused.

        """

        self.channel.exchange_delete(exchange=self.exchange,
                                     if_unused=if_unused)


class RabbitMQCon(RabbitMQPub):

    """Class:  RabbitMQCon

    Description:  Class which is a representation of a RabbitMQ Consumer, to
        include setting upa consumer callback capability and starting a
        loop to look for new messages in a message queue.  A RabbitMQCon object
        is used as proxy to implement the consuming a message from a RabbitMQ
        queue.

    Methods:
        __init__
        consume
        start_loop
        ack

    """

    def __init__(self, user, japd, host="localhost", port=5672, **kwargs):

        """Method:  __init__

        Description:  Initialization of an instance of the RabbitMQCon class.

        Arguments:
            (input) user -> User login name.
            (input) japd -> User psword.
            (input) host -> Hostname of RabbitMQ node.
            (input) port -> RabbitMQ port.  Default = 5672.
            (input) **kwargs:
                exchange_name -> Name of exchange.
                exchange_type -> Types: direct, fanout, headers, and topic.
                queue_name -> Name of the queue to create.
                routing_key -> Name of queue to rout to.
                x_durable -> True|False - Exchange survives reboots.
                q_durable -> True|False - Queue survives reboots.
                auto_delete -> True|False - Auto-delete after consuming.
                no_ack -> True|False - Automatic acknowledgement.
                host_list -> List of RabbitMQ nodes in a cluster.
                heartbeat -> Time in seconds to keep connection alive.

        """

        super(RabbitMQCon, self).__init__(
            user, japd, host, port,
            exchange_name=kwargs.get("exchange_name", ""),
            exchange_type=kwargs.get("exchange_type", "direct"),
            queue_name=kwargs.get("queue_name", ""),
            routing_key=kwargs.get("routing_key", ""),
            x_durable=kwargs.get("x_durable", True),
            q_durable=kwargs.get("q_durable", True),
            auto_delete=kwargs.get("auto_delete", False),
            heartbeat=kwargs.get("heartbeat", 60),
            host_list=kwargs.get("host_list", list()))

        self.no_ack = kwargs.get("no_ack", False)

    def consume(self, func_call, **kwargs):

        """Method:  consume

        Description:  Call the Basic Consume callback function for the
            requested queue.

        Arguments:
            (input) func_call -> Name of the callback function.
            (input) **kwargs:
                queue -> Name of queue.
            (output) Return consumer tag that is returned from basic_consume.

        """

        queue = kwargs.get("queue", self.queue_name)

        if pika.__version__ < '1.0.0':
            return self.channel.basic_consume(func_call, queue, self.no_ack)

        return self.channel.basic_consume(queue, func_call,
                                          auto_ack=self.no_ack)

    def start_loop(self):

        """Method:  start_loop

        Description:  Start an indefinite loop on checking for new messages in
            a RabbitMQ queue.

        Arguments:

        """

        try:
            self.channel.start_consuming()

        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.close()

    def ack(self, tag):

        """Method:  ack

        Description:  Send an acknowledge for a specific message tag.

        Arguments:
            (input) tag -> Message tag number being acknowledged.

        """

        self.channel.basic_ack(delivery_tag=tag)


class RabbitMQBase(object):

    """Class:  RabbitMQBase

    Description:  Class which is a representation of a RabbitMQ API connection.
        Contains the default type of requests such as GET, PUT, POST, DELETE.

    Note:
        For the Requests authentication set up:
            http://docs.python-requests.org/en/latest/user/authentication/

    Methods:
        __init__
        api_get
        get
        api_put
        put
        api_post
        post
        api_delete
        delete

    """

    def __init__(self, user, japd, host="localhost", port=15672,
                 scheme="https"):

        """Method:  __init__

        Description:  Initialization of an instance of the RabbitMQ class.

        Arguments:
            (input) user -> User login name
            (input) japd -> User psword
            (input) host -> Hostname of RabbitMQ node
            (input) port -> RabbitMQ adminstration port - default is 15672
            (input) scheme -> Type of connection - default is https

        """

        self.name = user
        self.host = host
        self.port = port
        self.scheme = scheme
        self.url = self.scheme + "://" + self.host + ":" + str(self.port)
        self.auth = (self.name, japd)
        self.headers = {"Content-type": "application/json"}

    def api_get(self, url_cmd, **kwargs):

        """Method:  api_get

        Description:  Wrapper for the request GET method call, also sets up
            headers, auth and base url.

        Arguments:
            (input) url_cmd -> GET command
            (input) kwargs:
                headers -> Additional headers to be added to base url
            (output) Response of the get command in dictionary format

        """

        kwargs["url"] = self.url + url_cmd
        kwargs["auth"] = self.auth
        headers = copy.deepcopy(self.headers)
        headers.update(kwargs.get("headers", {}))
        kwargs["headers"] = headers

        return self.get(**kwargs)

    def get(self, *args, **kwargs):

        """Method:  get

        Description:  Request GET command.

        Arguments:
            (input) kwargs:
                url -> Base url
                auth -> Authentication tuple
                headers -> Header commands
            (output) Response of the get command in dictionary format

        """

        response = requests.get(*args, **kwargs)
        response.raise_for_status()

        return response.json()

    def api_put(self, url_cmd, **kwargs):

        """Method:  api_put

        Description:  Wrapper for the request PUT method call, also sets up
            headers, auth and base url.

        Arguments:
            (input) url_cmd -> PUT command
            (input) kwargs:
                headers -> Additional headers to be added to base url
                data -> Data for the PUT command

        """

        kwargs["url"] = self.url + url_cmd
        kwargs["auth"] = self.auth
        headers = copy.deepcopy(self.headers)
        headers.update(kwargs.get("headers", {}))
        kwargs["headers"] = headers
        self.put(**kwargs)

    def put(self, *args, **kwargs):

        """Method:  put

        Description:  Request PUT command and also encode the JSON data.

        Arguments:
            (input) kwargs:
                url -> Base url
                auth -> Authentication tuple
                headers -> Header commands
                data -> Data for the PUT command

        """

        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])

        response = requests.put(*args, **kwargs)
        response.raise_for_status()

    def api_post(self, url_cmd, **kwargs):

        """Method:  api_post

        Description:  Wrapper for the request POST method call, also sets up
            headers, auth and base url.

        Arguments:
            (input) url_cmd -> POST command
            (input) kwargs:
                headers -> Additional headers to be added to base url
                data -> Data for the PUT command

        """

        kwargs["url"] = self.url + url_cmd
        kwargs["auth"] = self.auth
        headers = copy.deepcopy(self.headers)
        headers.update(kwargs.get("headers", {}))
        kwargs["headers"] = headers
        self.post(**kwargs)

    def post(self, *args, **kwargs):

        """Method:  post

        Description:  Request POST command and also encode the JSON data.

        Arguments:
            (input) kwargs:
                url -> Base url
                auth -> Authentication tuple
                headers -> Header commands
                data -> Data for the PUT command

        """

        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])

        response = requests.post(*args, **kwargs)
        response.raise_for_status()

    def api_delete(self, url_cmd, **kwargs):

        """Method:  api_delete

        Description:  Wrapper for the request DELETE method call, also sets up
            headers, auth and base url.

        Arguments:
            (input) url_cmd -> DELETE command
            (input) kwargs:
                headers -> Additional headers to be added to base url

        """

        kwargs["url"] = self.url + url_cmd
        kwargs["auth"] = self.auth
        headers = copy.deepcopy(self.headers)
        headers.update(kwargs.get("headers", {}))
        kwargs["headers"] = headers
        self.delete(**kwargs)

    def delete(self, *args, **kwargs):

        """Method:  delete

        Description:  Request DELETE command.

        Arguments:
            (input) kwargs:
                url -> Base url
                auth -> Authentication tuple
                headers -> Header commands

        """

        response = requests.delete(*args, **kwargs)
        response.raise_for_status()


class RabbitMQAdmin(RabbitMQBase):

    """Class:  RabbitMQAdmin

    Description:  Class which contains a list of RabbitMQ administration
        commands and uses the RabbitMQBase class as an entry point to
        RabbitMQ.

    Methods:
        overview
        get_cluster_name
        list_nodes
        get_node
        list_extensions
        get_definitions
        post_definitions
        list_connections
        get_connection
        delete_connection
        list_connection_channels
        list_channels
        get_channel
        list_consumers
        list_consumers_for_vhost
        list_exchanges
        list_exchanges_for_vhost
        get_exchange_for_vhost
        create_exchange_for_vhost
        delete_exchange_for_vhost
        list_bindings
        list_bindings_for_vhost
        list_vhosts
        get_vhost
        delete_vhost
        create_vhost
        list_users
        get_user
        delete_user
        create_user
        list_user_permissions
        whoami
        list_permissions
        get_vhost_user_perms
        delete_user_permission
        create_user_permission
        list_policies
        list_policies_for_vhost
        get_policy_for_vhost
        create_policy_for_vhost
        delete_policy_for_vhost
        is_vhost_alive
        list_topic_permissions
        list_vhost_topic_permissions
        list_user_topic_permissions
        list_vhost_user_topic_perms
        create_topic_permission
        delete_topic_permission
        create_queue_for_vhost
        get_queue_for_vhost
        list_queues
        list_queues_for_vhost
        delete_queue_for_vhost

    """

    def overview(self):

        """Method:  overview

        Description:  Returns information that describes the whole RabbitMQ
            server.

        Arguments:
            (output) Response of the command in dictionary format

        """

        return self.api_get("/api/overview")

    def get_cluster_name(self):

        """Method:  get_cluster_name

        Description:  Returns the name identifying the RabbitMQ cluster.

        Arguments:
            (output) RabbitMQ cluster name

        """

        return self.get(
            url=self.url + "/api/cluster-name", headers=self.headers,
            auth=self.auth)

    def list_nodes(self):

        """Method:  list_nodes

        Description:  Returns a list of nodes in the RabbitMQ cluster.  Set
        "memory=true" to get memory statistics, and "binary=true" to get a
        breakdown of binary memory use (may be expensive if there are many
        small binaries in the system).

        Arguments:
            (output) List of nodes in list format

        """

        return self.api_get("/api/nodes")

    def get_node(self, name, memory=False, binary=False):

        """Method:  get_node

        Description:  Returns information on a specify node.

        Arguments:
            (input) name -> Name of node
            (input) memory -> True|False - Return memory statistics
            (input) binary -> True|False - Return binary memory use
            (output) Returns information on node in dictionary format

        """

        return self.api_get(
            url_cmd="/api/nodes/{0}".format(name),
            params=dict(binary=binary, memory=memory))

    def list_extensions(self):

        """Method:  list_extensions

        Description:  Returns a list of extensions for the management plugin.

        Arguments:
            (output) List of extensions in list format

        """

        return self.api_get("/api/extensions")

    def get_definitions(self):

        """Method:  get_definitions

        Description:  Returns the server definitions that will include:
            exchanges, queues, bindings, users, virtual hosts, permissions
            and parameters.

        Note:  This method can be used for backing up the configuration of a
            server or cluster.

        Arguments:
            (output) Server definitions in dictionary format

        """

        return self.api_get("/api/definitions")

    def post_definitions(self, data):

        """Method:  post_definitions

        Description:  Post server definitions that will include: exchanges,
            queues, bindings, users, virtual hosts, permissions and parameters.
            POST to upload an existing set of definitions.

        Notes:
            1. This method can be used for restoring the configuration of a
                server or cluster.
            2. The definitions are merged. Anything already existing on the
                server but not in the uploaded definitions is untouched.
            3. Conflicting definitions on immutable objects (exchanges, queues
                and bindings) will cause an error.
            4. Conflicting definitions on mutable objects will cause the object
                in the server to be overwritten with the object from the
                definitions.
            5. In the event of an error you will be left with a part-applied
                set of definitions.
            6. No post to messages is done.

        Arguments:
            (input) data -> Definitions

        """

        self.api_post("/api/definitions", data=data)

    def list_connections(self):

        """Method:  list_connections

        Description:  Returns a list of all open connections.

        Arguments:
            (output) List of connections in list format

        """

        return self.api_get("/api/connections")

    def get_connection(self, name):

        """Method:  get_connection

        Description:  Returns information on a single connection.

        Arguments:
            (input) name -> Name of connection
            (output) Information on connection in dictionary format

        """

        return self.api_get(
            "/api/connections/{0}".format(urllib.parse.quote_plus(name)))

    def delete_connection(self, name, reason=None):

        """Method:  delete_connection

        Description:  Delete named connection, with optional reason.

        Arguments:
            (input) name -> Name of connection
            (input) reason -> Reason for delete

        """

        headers = {'X-Reason': reason} if reason else {}

        self.api_delete(
            "/api/connections/{0}".format(
                urllib.parse.quote_plus(name)), headers=headers)

    def list_connection_channels(self, name):

        """Method:  list_connection_channels

        Description:  Lists all channels for a specific connection.

        Arguments:
            (input) name -> Name of connection
            (output) List of channels for connection

        """

        return self.api_get(
            "/api/connections/{0}/channels".format(
                urllib.parse.quote_plus(name)))

    def list_channels(self):

        """Method:  list_channels

        Description:  Returns a list of all open channels.

        Arguments:
            (output) List of channels in list format

        """

        return self.api_get("/api/channels")

    def get_channel(self, name):

        """Method:  get_channel

        Description:  Lists information for a specific channel.

        Arguments:
            (input) name -> Name of channel
            (output) Information on a channel in dictionary format

        """

        return self.api_get(
            "/api/channels/{0}".format(urllib.parse.quote_plus(name)))

    def list_consumers(self):

        """Method:  list_consumers

        Description:  Returns a list of all consumers.

        Arguments:
            (output) List of consumers in list format

        """

        return self.api_get("/api/consumers")

    def list_consumers_for_vhost(self, vhost):

        """Method:  list_consumers_for_vhost

        Description:  Lists all customers for a specific virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (output) List of consumers in list format

        """

        return self.api_get(
            "/api/consumers/{0}".format(urllib.parse.quote_plus(vhost)))

    def list_exchanges(self):

        """Method:  list_exchanges

        Description:  Returns a list of all exchanges.

        Arguments:
            (output) List of exchanges in list format

        """

        return self.api_get("/api/exchanges")

    def list_exchanges_for_vhost(self, vhost):

        """Method:  list_exchanges_for_vhost

        Description:  Lists all exchanges for a specific virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (output) List of exchanges in list format

        """

        return self.api_get(
            "/api/exchanges/{0}".format(urllib.parse.quote_plus(vhost)))

    def get_exchange_for_vhost(self, exchange, vhost):

        """Method:  get_exchange_for_vhost

        Description:  Return information on an individual exchange in a
            specific virtual host.

        Arguments:
            (input) exchange -> Name of exchange
            (input) vhost -> Name of virtual host
            (output) Information on exchange in vhost in dictionary format

        """

        return self.api_get(
            "/api/exchanges/{0}/{1}".format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(exchange)))

    def create_exchange_for_vhost(self, exchange, vhost, body):

        """Method:  create_exchange_for_vhost

        Description:  Creates an exchange on a virtual host.

        Notes:
            1. Body will have the following format:
                {"type": "direct",
                 "auto_delete": false,
                 "durable": true,
                 "internal": false,
                 "arguments": {}}
            2. The type key is mandatory; other keys are optional.

        Arguments:
            (input) exchange -> Name of exchange
            (input) vhost -> Name of virtual host
            (input) body -> Dictionary of attributes for exchange creation

        """

        self.api_put(
            "/api/exchanges/{0}/{1}".format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(exchange)), data=body)

    def list_bindings(self):

        """Method:  list_bindings

        Description:  Returns a list of all bindings.

        Arguments:
            (output) List of bindings in list format

        """

        return self.api_get("/api/bindings")

    def list_bindings_for_vhost(self, vhost):

        """Method:  list_bindings_for_vhost

        Description:  Lists all bindings for a specific virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (output) List of bindings in list format

        """

        return self.api_get(
            "/api/bindings/{}".format(urllib.parse.quote_plus(vhost)))

    def list_vhosts(self):

        """Method:  list_vhosts

        Description:  Returns a list of all virtual hosts.

        Arguments:
            (output) List of virtual hosts in list format

        """

        return self.api_get("/api/vhosts")

    def get_vhost(self, vhost):

        """Method:  get_vhost

        Description:  Return information for a specific virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (output) Information on virtual host in dictionary format

        """

        global API_VHOST

        return self.api_get(API_VHOST.format(urllib.parse.quote_plus(vhost)))

    def delete_vhost(self, vhost):

        """Method:  delete_vhost

        Description:  Delete a virtual host.

        Arguments:
            (input) vhost -> Name of virtual host

        """

        global API_VHOST

        self.api_delete(API_VHOST.format(urllib.parse.quote_plus(vhost)))

    def create_vhost(self, vhost, tracing=False):

        """Method:  create_vhost

        Description:  Create a virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (input) tracing -> True|False - Enable tracing in the host

        """

        global API_VHOST

        data = {"tracing": True} if tracing else {}

        self.api_put(
            API_VHOST.format(urllib.parse.quote_plus(vhost)), data=data)

    def list_users(self):

        """Method:  list_users

        Description:  Return a list of users.

        Arguments:
            (output) List of users in list format

        """

        return self.api_get("/api/users")

    def get_user(self, name):

        """Method:  get_user

        Description:  Return information for an individual user.

        Arguments:
            (input) name -> Name of user
            (output) Information on individual user in dictionary format

        """

        global API_USER

        return self.api_get(API_USER.format(urllib.parse.quote_plus(name)))

    def delete_user(self, name):

        """Method:  delete_user

        Description:  Delete an individual user.

        Arguments:
            (input) name -> Name of user

        """

        global API_USER

        self.api_delete(API_USER.format(urllib.parse.quote_plus(name)))

    def create_user(self, name, japd, japd_hash=None, tags=None):

        """Method:  create_user

        Description:  Create an individual user.

        Arguments:
            (input) name -> Name of user
            (input) japd -> User pswd, set to "" if no pswd is required
                The japd argument takes precedence if japd_hash is also set
            (input) japd_hash -> An optional pswd hash for the user
            (input) tags -> List of tags for user
                Currently recognized tags are:
                    "administrator", "monitoring" and "management"
                If no tags are supplied, then no permission is assigned to user

        """

        global KEY1
        global KEY2
        global KEY3
        global API_USER

        data = {"tags": ", ".join(tags or [])}

        if japd:
            data[KEY1 + KEY2] = japd

        elif japd_hash:
            data[KEY1 + KEY2 + KEY3] = japd_hash

        else:
            data[KEY1 + KEY2 + KEY3] = ""

        self.api_put(API_USER.format(urllib.parse.quote_plus(name)), data=data)

    def list_user_permissions(self, name):

        """Method:  list_user_permissions

        Description:  List of permissions for a specific user.

        Arguments:
            (input) name -> Name of user
            (output) List of permissions for user in list format

        """

        return self.api_get(
            "/api/users/{0}/permissions".format(urllib.parse.quote_plus(name)))

    def whoami(self):

        """Method:  whoami

        Description:  Information on the current user.

        Arguments:
            (output) Return information on current user in dictionary format

        """

        return self.api_get("/api/whoami")

    def list_permissions(self):

        """Method:  list_permissions

        Description:  Lists all permissions for all users.

        Arguments:
            (output) Return permissions on all users in list format

        """

        return self.api_get("/api/permissions")

    def get_vhost_user_perms(self, vhost, name):

        """Method:  get_vhost_user_perms

        Description:  Get user permissions on a specific virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (input) name -> Name of user
            (output) Returns user permissions on a vhost in dictionary format

        """

        global API_PERM

        return self.api_get(
            API_PERM.format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)))

    def delete_user_permission(self, name, vhost):

        """Method:  delete_user_permission

        Description:  Delete an user's permissions on a specific virtual host.

        Arguments:
            (input) name -> User name
            (input) vhost -> Name of virtual host

        """

        global API_PERM

        self.api_delete(
            API_PERM.format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)))

    def create_user_permission(self, name, vhost, configure=None, write=None,
                               read=None):

        """Method:  create_user

        Description:  Create an individual user.

        Arguments:
            (input) name -> Name of user
            (input) vhost -> Name of virtual host
            (input) configure -> Regex for the user permission, default is `.*`
            (input) write -> Regex for the user permission, default is `.*`
            (input) read -> Regex for the user permission, default is `.*`

        """

        global API_PERM

        data = {
            "configure": configure or '.*',
            "write": write or '.*',
            "read": read or '.*'}

        self.api_put(
            API_PERM.format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)),
            data=data)

    def list_policies(self):

        """Method:  list_policies

        Description:  List of all the policies.

        Arguments:
            (output) List of policies in list format

        """

        return self.api_get("/api/policies")

    def list_policies_for_vhost(self, name):

        """Method:  list_policies_for_vhost

        Description:  List of all the policies for a specific virtual host.

        Arguments:
            (input) name -> Name of virtual host
            (output) List of policies for a vhost in list format

        """

        return self.api_get(
            "/api/policies/{0}".format(urllib.parse.quote_plus(name)))

    def get_policy_for_vhost(self, vhost, name):

        """Method:  get_policy_for_vhost

        Description:  Details for a policy for a specific virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (input) name -> Name of policy
            (output) Details on a policy for a vhost in dictionary format

        """

        return self.api_get(
            "/api/policies/{0}/{1}".format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)))

    def create_policy_for_vhost(self, vhost, name, definition, pattern=None,
                                priority=0, apply_to='all'):

        """Method:  create_policy_for_vhost

        Description:  Create a policy on a specific virtual host.

        Example:
            # Makes all queues and exchanges on vhost "/" highly available
            api.create_policy_for_vhost(
                vhost="/",
                name="ha-all",
                definition={"ha-mode": "all"},
                pattern="",
                apply_to="all")

        Arguments:
            (input) vhost -> Name of virtual host
            (input) name -> Name of policy
            (input) definition -> Definition of the policy in dictionary format
            (input) pattern -> Pattern of resource names to apply the policy to
            (input) priority -> Priority of policy, default is 0
            (input) apply_to -> What resource type to apply the policy to
                Typical values: exchanges, queues, all

        """

        data = {"pattern": pattern, "definition": definition,
                "priority": priority, "apply-to": apply_to}

        self.api_put(
            "/api/policies/{0}/{1}".format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)),
            data=data)

    def delete_policy_for_vhost(self, vhost, name):

        """Method:  delete_policy_for_vhost

        Description:  Delete a specific policy on a virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (input) name -> Policy name

        """

        self.api_delete(
            "/api/policies/{0}/{1}/".format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)))

    def is_vhost_alive(self, vhost):

        """Method:  is_vhost_alive

        Description:  Declares a test queue, then publishes and consumes a
            message.

        Notes:  This is intended for use by monitoring tools.

        Arguments:
            (input) vhost -> Name of virtual host
            (output) Returns status of vhost in dictionary format

        """

        return self.api_get(
            "/api/aliveness-test/{0}".format(urllib.parse.quote_plus(vhost)))

    def list_topic_permissions(self):

        """Method:  list_topic_permissions

        Description:  List of all topic permissions for all users.

        Arguments:
            (output) List of topic permissions in list format

        """

        return self.api_get("/api/topic-permissions")

    def list_vhost_topic_permissions(self, name):

        """Method:  list_vhost_topic_permissions

        Description:  List all topic permissions for a specific virtual host.

        Arguments:
            (input) name -> Name of virtual host
            (output) List of topic permissions for a vhost in list format

        """

        return self.api_get(
            "/api/vhosts/{0}/topic-permissions".format(
                urllib.parse.quote_plus(name)))

    def list_user_topic_permissions(self, name):

        """Method:  list_user_topic_permissions

        Description:  List of topic permissions for a specific user.

        Arguments:
            (input) name -> Name of user
            (output) List of topic permissions for user in list format

        """

        return self.api_get(
            "/api/users/{0}/topic-permissions".format(
                urllib.parse.quote_plus(name)))

    def list_vhost_user_topic_perms(self, vhost, name):

        """Method:  list_vhost_user_topic_perms

        Description:  Get user topic permissions on a specific virtual host.

        Arguments:
            (input) vhost -> Name of virtual host
            (input) name -> Name of user
            (output) Returns user topic perms on a vhost in list format

        """

        return self.api_get(
            "/api/topic-permissions/{0}/{1}".format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)))

    def create_topic_permission(self, name, vhost, exchange, write="",
                                read=""):

        """Method:  create_topic_permission

        Description:  Create a topic permission.

        Notes:  For the read and write topic permissions, '' is a synonym for
            '^$' and restricts permissions in the exact same way.

        Arguments:
            (input) name -> Name of user
            (input) vhost -> Name of virtual host
            (input) exchange -> Exchange name
            (input) write -> Regex for the user permission, default is ""
            (input) read -> Regex for the user permission, default is ""

        """

        data = {"exchange": exchange, "read": read, "write": write}

        self.api_put(
            "/api/topic-permissions/{0}/{1}".format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)),
            data=data)

    def delete_topic_permission(self, name, vhost, exchange):

        """Method:  delete_topic_permission

        Description:  Delete a individual topic permission for a user on a
            virtual host on a named exchange.

        Arguments:
            (input) name -> User name
            (input) vhost -> Name of virtual host
            (input) exchange - Exchange name

        """

        self.api_delete(
            "/api/topic-permissions/{0}/{1}/{2}".format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name),
                urllib.parse.quote_plus(exchange)))

    def create_queue_for_vhost(self, name, vhost, body):

        """Method:  create_queue_for_vhost

        Description:  Create an individual queue in a virtual host.

        Notes:  The body should look like this.  All keys are optional.
            {"auto_delete":false,
             "durable":true,
             "arguments":{},
             "node":"rabbit@rabbit1"}

        Arguments:
            (input) name -> Name of queue
            (input) vhost -> Name of virtual host
            (input) body -> The body for the queue in dictionary format

        """

        global API_QUEUE

        self.api_put(
            API_QUEUE.format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)),
            data=body)

    def get_queue_for_vhost(self, name, vhost):

        """Method:  get_queue_for_vhost

        Description:  Get information on individual queue in a virtual host.

        Arguments:
            (input) name -> Name of queue
            (input) vhost -> Name of virtual host
            (output) Returns queue information on a vhost in dictionary format

        """

        global API_QUEUE

        return self.api_get(
            API_QUEUE.format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)))

    def list_queues(self):

        """Method:  list_queues

        Description:  Returns a list of all queues.

        Arguments:
            (output) Returns list of queues in list format

        """

        return self.api_get("/api/queues")

    def list_queues_for_vhost(self, name):

        """Method:  get_queue_for_vhost

        Description:  Get information on individual queue in a virtual host.

        Arguments:
            (input) name -> Name of virtual host
            (output) Returns list of queues on a vhost in list format

        """

        return self.api_get(
            "/api/queues/{0}".format(urllib.parse.quote_plus(name)))

    def delete_queue_for_vhost(self, name, vhost, if_unused=True,
                               if_empty=True):

        """Method:  delete_queue_for_vhost

        Description:  Delete and individual queue on a virtual host.

        Notes:
            1. if_unused=True: This prevents the delete from succeeding if the
                queue has consumers.  False will override this option.
            2. if_empty=True: This prevents the delete from succeeding if the
                queue contains messages.  False will override this option.

        Arguments:
            (input) name -> Name of queue
            (input) vhost -> Name of virtual host
            (input) if_unused -> True|False - Delete if queue is unused
            (input) if_empty -> True|False - Delete if queue is empty

        """

        global API_QUEUE

        self.api_delete(
            API_QUEUE.format(
                urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(name)),
            params={"if-unused": if_unused, "if-empty": if_empty})
