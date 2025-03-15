-- As explained on: https://bennett.dev/auto-link-pipewire-ports-wireplumber/
--
-- This script keeps my stereo-null-sink connected to whatever output I'm currently using.
-- I do this so Pulseaudio (and Wine) always sees a stereo output plus I can swap the output
-- without needing to reconnect everything.

-- Link two ports together
function link_port(output_port, input_port)
  if not input_port or not output_port then
    return nil
  end

  local link_args = {
    ["link.input.node"] = input_port.properties["node.id"],
    ["link.input.port"] = input_port.properties["object.id"],

    ["link.output.node"] = output_port.properties["node.id"],
    ["link.output.port"] = output_port.properties["object.id"],
    
    -- The node never got created if it didn't have this field set to something
    ["object.id"] = nil,

    -- I was running into issues when I didn't have this set
    ["object.linger"] = true,

    ["node.description"] = "Link created by auto_connect_ports"
  }

  local link = Link("link-factory", link_args)
  link:activate(1)

  return link
end

-- Automatically link ports together by their specific audio channels.
--
-- ┌──────────────────┐         ┌───────────────────┐
-- │                  │         │                   │
-- │               FL ├────────►│ AUX0              │
-- │      SOURCE      │         │                   │
-- │               FR ├────────►│ AUX1   SINK       │
-- │                  │         │                   │
-- └──────────────────┘         │ AUX2              │
--                              │                   │
--                              └───────────────────┘
-- 
-- -- Call this method inside a script in global scope
--
-- auto_connect_ports {
--
--   -- A constraint for all the required ports of the output device 
--   source = Constraint { .. }
--
--   -- A constraint for all the required ports of the input device 
--   sink = Constraint { .. }
--
--   -- A mapping of output audio channels to input audio channels
--
--   connections = {
--     FL = "AUX0"
--     FR = "AUX1"
--   }
--
-- }
--
function auto_connect_ports(args)
  local source_om = ObjectManager {
    Interest {
      type = "port",
      args["source"],
    }
  }

  local sink_om = ObjectManager {
    Interest {
      type = "port",
      args["sink"],
    }
  }

  local all_links = ObjectManager {
    Interest {
      type = "link",
    }
  }

  function _connect()
    print("_connect")
    for source_name, sink_name in pairs(args.connect) do
      print(source_name, sink_name)
      for source in source_om:iterate { Constraint { "port.name", "equals", source_name } } do
	print(source)
       	for sink in sink_om:iterate { Constraint { "port.name", "equals", sink_name } } do
	  print(sink)
          local link = link_port(source, sink)
 	  if link then
            print("link")
    	  else
	    print("no link")
    	  end
        end
      end
    end
  end

  source_om:connect("object-added", _connect)
  sink_om:connect("object-added", _connect)
  all_links:connect("object-added", _connect)

  source_om:activate()
  sink_om:activate()
  all_links:activate()
end

auto_connect_ports {
  source = Constraint { "object.path", "matches", "virtual_in:*" },
  sink = Constraint { "port.alias", "matches", "ALC671 Analog:*" },
  connect = {
    monitor_FL = "playback_FL",
    monitor_FR = "playback_FR"
  }
}

auto_connect_ports {
  source = Constraint { "object.path", "matches", "virtual_in:*" },
  sink = Constraint { "object.path", "matches", "virtualx_in:*" },
  connect = {
    monitor_FL = "playback_1",
    monitor_FR = "playback_2"
  }
}
auto_connect_ports {
  source = Constraint { "object.path", "matches", "rnnoise_source:*" },
  sink = Constraint { "object.path", "matches", "virtualx_in:*" },
  connect = {
    capture_MONO = "playback_3",
  }
}
