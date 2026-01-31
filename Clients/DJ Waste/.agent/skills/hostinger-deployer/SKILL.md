---
name: hostinger-deployer
description: Deploys static/Vite sites to Hostinger using the "Zip & Ship" SSH method.
---
# Hostinger Deployment Skill

This skill handles the end-to-end deployment of static or Vite-based applications to Hostinger using a robust "Zip & Ship" method via SFTP/SSH.

## Workflow

1.  **Build**: Generates the production build (usually `dist` folder).
2.  **Compress**: Zips the build output into a deployment archive.
3.  **Ship**: Uploads the archive and a helper PHP script to the server via SFTP.
4.  **Extract**: Triggers the PHP script to unzip the archive on the server and move files to the correct location.
5.  **Cleanup**: The PHP script automatically deletes the zip and itself.

## Usage

### Prerequisites
- SSH Credentials (IP, Port, Username, Password)
- Access to the `curl` command with SFTP support.
- A PHP-enabled Hostinger shared hosting environment.

### Steps

1.  **Prepare Build**
    ```powershell
    npm install
    npm run build
    ```

2.  **Zip Output**
    ```powershell
    Compress-Archive -Path "dist\public\*" -DestinationPath "site_deploy.zip" -Force
    ```

3.  **Create Unzip Script** (`unzip.php`)
    ```php
    <?php
    $zip = new ZipArchive;
    if ($zip->open('site_deploy.zip') === TRUE) {
        $zip->extractTo('./');
        $zip->close();
        echo 'Deployment Complete';
        unlink('site_deploy.zip');
        unlink(__FILE__);
    } else {
        echo 'Extraction Failed';
    }
    ?>
    ```

4.  **Upload Files**
    ```powershell
    # Upload Zip
    curl -k -T "site_deploy.zip" -u "USER:PASS" "sftp://IP:PORT/path/to/public_html/site_deploy.zip"
    
    # Upload Script
    curl -k -T "unzip.php" -u "USER:PASS" "sftp://IP:PORT/path/to/public_html/unzip.php"
    ```

5.  **Execute Deployment**
    ```powershell
    curl -k "https://your-domain.com/unzip.php"
    ```

## Common Configs (DJ Waste)
- **IP**: 92.112.189.250
- **Port**: 65002
- **User**: u384342620
- **Path**: /home/u384342620/domains/dj-waste.co.uk/public_html/

## Troubleshooting
- **White Screen**: 
    - Check `import.meta.env` usage.
    - **CRITICAL**: Remove Manus/debug plugins from `vite.config.ts` in production as they inject massive runtime scripts that can crash the app.
    - Verify `base` in `vite.config.ts` is correct (usually `/`).
- **403 Forbidden**: Check file permissions or missing `index.php`/`index.html`.
- **curl: (78) No such file**: The SFTP path is likely wrong. Use the absolute home directory path: `/home/USERNAME/domains/DOMAIN.COM/public_html/`.
- **Assets Not Updating**: Ensure the `unzip.php` script deletes the `assets/` and `images/` folders before extraction to prevent permission/overwrite conflicts.
- **Cached Content**: Clear browser cache or Cloudflare cache if applicable.
