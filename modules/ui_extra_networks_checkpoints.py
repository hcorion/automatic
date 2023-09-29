import html
import json
import os
from modules import shared, ui_extra_networks, sd_models


class ExtraNetworksPageCheckpoints(ui_extra_networks.ExtraNetworksPage):
    def __init__(self):
        super().__init__('Model')

    def refresh(self):
        shared.refresh_checkpoints()

    def list_items(self):
        checkpoint: sd_models.CheckpointInfo
        for name, checkpoint in sd_models.checkpoints_list.items():
            fn = os.path.splitext(checkpoint.filename)[0]
            record = {
                "type": 'Model',
                "name": checkpoint.name,
                "title": checkpoint.title,
                "filename": checkpoint.filename,
                "hash": checkpoint.shorthash,
                "search_term": self.search_terms_from_path(checkpoint.title),
                "preview": self.find_preview(fn),
                "local_preview": f"{fn}.{shared.opts.samples_format}",
                "description": self.find_description(fn),
                "info": self.find_info(fn),
                "metadata": checkpoint.metadata,
                "onclick": '"' + html.escape(f"""return selectCheckpoint({json.dumps(name)})""") + '"',
            }
            yield record

    def allowed_directories_for_previews(self):
        return [v for v in [shared.opts.ckpt_dir, shared.opts.diffusers_dir, sd_models.model_path] if v is not None]
