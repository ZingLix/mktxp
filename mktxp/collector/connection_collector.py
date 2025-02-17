# coding=utf8
## Copyright (c) 2020 Arseniy Kuznetsov
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.


from mktxp.collector.base_collector import BaseCollector
from mktxp.flow.processor.output import BaseOutputProcessor
from mktxp.datasource.connection_ds import (
    IPConnectionDatasource,
    IPConnectionStatsDatasource,
    IPConnectionRateDatasource,
)


class IPConnectionCollector(BaseCollector):
    """ IP Connection Metrics collector
    """

    @staticmethod
    def collect(router_entry):
        if router_entry.config_entry.connections:
            connection_records = IPConnectionDatasource.metric_records(router_entry)
            if connection_records:
                connection_metrics = BaseCollector.gauge_collector(
                    "ip_connections_total",
                    "Number of IP connections",
                    connection_records,
                    "count",
                )
                yield connection_metrics

        if router_entry.config_entry.connection_stats:
            connection_stats_records = IPConnectionStatsDatasource.metric_records(
                router_entry
            )

            for connection_stat_record in connection_stats_records:
                BaseOutputProcessor.augment_record(
                    router_entry, connection_stat_record, id_key="src_address"
                )

            connection_stats_labels = ["src_address", "dst_addresses", "dhcp_name"]
            connection_stats_metrics_gauge = BaseCollector.gauge_collector(
                "connection_stats",
                "Open connection stats",
                connection_stats_records,
                "connection_count",
                connection_stats_labels,
            )
            yield connection_stats_metrics_gauge

            connection_rate_records = IPConnectionRateDatasource.metric_records(
                router_entry
            )
            connection_rates_labels = [
                "src_ip",
                "src_address",
                "dst_address",
                "protocol",
            ]
            connection_recv_rates_metrics_gauge = BaseCollector.gauge_collector(
                "connection_recv_rate",
                "Open connection recv rates",
                connection_rate_records,
                "repl-rate",
                connection_rates_labels,
            )
            yield connection_recv_rates_metrics_gauge
            connection_send_rates_metrics_gauge = BaseCollector.gauge_collector(
                "connection_send_rate",
                "Open connection sebd rates",
                connection_rate_records,
                "orig-rate",
                connection_rates_labels,
            )
            yield connection_send_rates_metrics_gauge
            connection_recv_bytes_metrics_gauge = BaseCollector.gauge_collector(
                "connection_recv_bytes",
                "Open connection recv rates",
                connection_rate_records,
                "repl-bytes",
                connection_rates_labels,
            )
            yield connection_recv_bytes_metrics_gauge
            connection_send_bytes_metrics_gauge = BaseCollector.gauge_collector(
                "connection_send_bytes",
                "Open connection sebd rates",
                connection_rate_records,
                "orig-bytes",
                connection_rates_labels,
            )
            yield connection_send_bytes_metrics_gauge

